"""Utilities for run epilogs"""
from __future__ import annotations

import concurrent.futures
import threading
from logging import INFO
from typing import Any, Callable, Dict, Generator, List, NamedTuple, Optional, Tuple, Union

from kubernetes import client
from rich.progress import Progress, SpinnerColumn, TaskID, TextColumn, TimeElapsedColumn

from mcli.utils.utils_kube import deserialize, get_rank0_pod, robust_stream_events, wait_for_job_pods
from mcli.utils.utils_kube_labels import label
from mcli.utils.utils_logging import FAIL, get_indented_block
from mcli.utils.utils_pod_state import PodState, PodStatus


class ContextPodStatus(NamedTuple):
    """Tuple of pod name, pod rank and pod status

    Useful for providing status for one pod in a multi-pod run
    """
    name: str
    rank: int
    status: PodStatus

    @classmethod
    def from_pod_dict(cls, pod_dict: Dict[str, Any]) -> ContextPodStatus:
        """Create a ``ContextPodStatus`` from the dictionary representation of a pod spec

        Args:
            pod_dict: Dictionary representation of a pod spec

        Returns:
            ``ContextPodStatus`` object
        """
        pod: client.V1Pod = deserialize(pod_dict, 'V1Pod')
        return cls.from_pod(pod)

    @classmethod
    def from_pod(cls, pod: client.V1Pod) -> ContextPodStatus:
        """Create a ``ContextPodStatus`` from a Kubernetes V1Pod object

        Args:
            pod: Kubernetes V1Pod object

        Returns:
            ``ContextPodStatus`` object
        """
        if pod.metadata is None:
            raise ValueError('UknownPod: Pod does not have metadata, so it has no name')
        name = pod.metadata.name
        if pod.metadata.annotations is not None:
            rank = int(pod.metadata.annotations.get(label.kube_batch.POD_RANK, '0'))
        else:
            rank = 0
        status = PodStatus.from_pod_status(pod.status)
        return cls(name=name, rank=rank, status=status)


def safe_next(iterable) -> Union[Any, StopIteration]:
    """Safely call `next` on an generator in a thread. If generator has finished,
    StopIteration is returned as a sentinel
    """
    try:
        return next(iterable)
    except StopIteration:
        return StopIteration


def concurrent_chain(*iters: Generator[Any, None, None],
                     shutdown: Optional[threading.Event] = None) -> Generator[Any, None, None]:
    """Chain multiple iterators that return asynchronously using concurrent futures

    Args:
        *iters: A sequence of iterators to chain together. Items will be returned unordered
        shutdown: Optional ``threading.Event`` flag that will be set on ``GeneratorExit``.
            Provide this ``Event`` to the iterators as well so they can be gracefully shutdown.

    Yields:
        Items from the chained iterators

    Note: If the subgenerators are compute intensive, you likely want to either manually
    shutdown using `shutdown.set()` or call `close()` on the chained generator
    """

    with concurrent.futures.ThreadPoolExecutor(len(iters)) as executor:
        futures_dict = {executor.submit(safe_next, it): it for it in iters}
        try:
            while futures_dict:
                f = concurrent.futures.wait(futures_dict, timeout=1)
                for fi in f.done:
                    # Optionally shutdown
                    if shutdown and shutdown.is_set():
                        return

                    # Get current one
                    value = fi.result()

                    # Remove finished future
                    it = futures_dict.pop(fi)

                    # If this iter is done, don't carry on
                    if value is StopIteration:
                        continue

                    yield value

                    # Add the next value
                    futures_dict[executor.submit(safe_next, it)] = it

                # Optionally shutdown after last yield
                if shutdown and shutdown.is_set():
                    return

        except GeneratorExit:
            if shutdown:
                shutdown.set()
            raise


def concurrent_watch_pod_events(namespace,
                                names: List[str],
                                timeout: Optional[int] = None) -> Generator[ContextPodStatus, None, None]:
    """Stream the pod status of multiple pods simulatenously

    Args:
        namespace: Namespace in which the pods live
        names: List of pod names
        timeout: Optional streaming timeout

    Yields:
        ContextPodStatus objects that contain the pod name, pod rank and pod status
    """

    api = client.CoreV1Api()
    shutdown = threading.Event()
    streams = [
        robust_stream_events(api.list_namespaced_pod,
                             namespace=namespace,
                             timeout=timeout,
                             field_selector=f'metadata.name={name}',
                             shutdown=shutdown) for name in names
    ]

    for pod in concurrent_chain(*streams, shutdown=shutdown):
        yield ContextPodStatus.from_pod(pod['object'])


class RunEpilog:
    """Helper for creating a run epilog that follows pod creation

    Args:
        name: Name of the run
        namespace: Namespace in which the run lives
    """

    _default_fail_states: Tuple[PodState, ...] = (PodState.FAILED, PodState.FAILED_PULL)

    def __init__(self, name: str, namespace: str):
        self.name = name
        self.namespace = namespace
        self.pod_names = wait_for_job_pods(name, namespace)
        self._rank0_pod: Optional[str] = None

    @property
    def rank0_pod(self) -> str:
        """The rank 0 pod for the run
        """
        if self._rank0_pod is None:
            self._rank0_pod = get_rank0_pod(self.name, self.namespace)
        return self._rank0_pod

    def wait_until(
        self,
        callback: Optional[Callable[[ContextPodStatus], None]] = None,
        fail_states: Optional[List[PodState]] = None,
        pass_state: Optional[PodState] = PodState.RUNNING,
        timeout: Optional[int] = None,
    ) -> Optional[PodStatus]:
        """Wait for the lifecycle(s) of the run's pod(s) to reach certain conditions

        If a single pod reaches a state listed in ``fail_states``, that pod's status will be
        returned. If all pods reach or surpass the ``pass_state``, the final
        pod's status will be returned.

        Args:
            callback: Function to call with each ``ContextPodStatus`` object in the stream.
                Defaults to None.
            fail_states: List of ``PodState``s to fail on. Triggers the return of a
                ``PodStatus`` object whenever ANY pod hits one of these states.
                Defaults to [PodState.FAILED, PodState.FAILED_PULL].
            pass_state: ``PodState`` to pass on. Triggers the return of a
                ``PodStatus`` object whenever ALL pods reach or surpass this state.
                Defaults to PodState.RUNNING.
            timeout: Timeout for how long to wait, in seconds. Defaults to None.

        Returns:
            If the timeout isn't reached, returns the final pod's ``PodStatus`` object
        """
        if fail_states is None:
            fail_states = list(self._default_fail_states)

        all_states: Dict[int, Optional[PodState]] = {rank: None for rank in range(len(self.pod_names))}
        for pod_status in concurrent_watch_pod_events(namespace=self.namespace, names=self.pod_names, timeout=timeout):
            if self._rank0_pod is None and pod_status.rank == 0:
                self._rank0_pod = pod_status.name

            if callback:
                callback(pod_status)

            if fail_states and pod_status.status.state in fail_states:
                return pod_status.status

            all_states[pod_status.rank] = pod_status.status.state
            if pass_state and all(st and st.after(pass_state, inclusive=True) for st in all_states.values()):
                return pod_status.status


class EpilogSpinner:
    """A multi-pod spinner for use as a callback to ``RunEpilog``

    This can be used as a context manager where the spinner(s) will be started and
    stopped automatically. Otherwise they can be manually started and stopped using
    ``spinner.progress.start()`` and ``spinner.progress.stop()``.

    Attributes:
        progress: The ``rich.progress`` progress bar that contains the spinners

    Example:

    epilog = RunEpilog(run_name, namespace)
    with EpilogSpinner() as spinner:
        last_status = epilog.wait_until(callback=spinner, timeout=300)
    """

    def __init__(self):
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn('[progress.description]{task.description}'),
            TimeElapsedColumn(),
            transient=True,
        )
        self._tasks: Dict[int, TaskID] = {}

    def __enter__(self) -> EpilogSpinner:
        self.progress.start()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb) -> bool:
        self.progress.stop()
        return False

    def _make_tasks(self, rank: int):
        for ii in range(rank):
            self._make_tasks(ii)
        if rank not in self._tasks:
            self._tasks[rank] = self.progress.add_task(description='Rank')

    @staticmethod
    def _get_description(state: PodState) -> str:
        if state == PodState.QUEUED:
            return 'Waiting for resources to become available...'
        elif state == PodState.STARTING:
            return 'Pulling Docker image...'
        elif state == PodState.SCHEDULED:
            return 'Instance found. Waiting for run to start...'
        elif state == PodState.FAILED_PULL:
            return 'Failed to pull Docker image...'
        else:
            return state.value.title().replace('_', ' ') + '...'

    @staticmethod
    def _format_rank_description(rank: int, desc: str) -> str:
        return f'Rank {rank}: {desc}'

    def __call__(self, status: ContextPodStatus):
        rank = status.rank
        self._make_tasks(rank)
        state = status.status.state
        desc = self._format_rank_description(rank, self._get_description(state))
        self.progress.update(self._tasks[rank], description=desc)


class CommonLog():
    """Log some common epilog log outputs
    """

    def __init__(self, logger):
        self.logger = logger

    def log_timeout(self):
        self.logger.warning(('Run is taking awhile to start, returning you to the command line.\n'
                             'Common causes are the run is queued because the resources are not available '
                             'yet, or the docker image is taking awhile to download.\n\n'
                             'To continue to view job status, use `mcli get runs` and `mcli logs`.'))

    def log_pod_failed_pull(self, run_name: str, image: str):
        self.logger.error(f'{FAIL} Run {run_name} failed to start and will be deleted because it could '
                          'still be consuming resources.')

        error_message = f"""
                    Could not find Docker image "{image}". If this is a private image, check
                    `mcli get secret` to ensure that you have a Docker secret created. If not, create one
                    using `mcli create secret docker`. Otherwise, double-check your image name.
                """
        self.logger.error(get_indented_block(error_message))

    def log_pod_failed(self, run_name: str):
        self.logger.error(f'{FAIL} Run {run_name} failed. You can check its logs using '
                          f'`mcli logs {run_name}`')

    def log_unknown_did_not_start(self):
        self.logger.warning(f'{INFO} Run did not start for an unknown reason. You can monitor it with '
                            '`mcli get runs` to see if it starts.')
