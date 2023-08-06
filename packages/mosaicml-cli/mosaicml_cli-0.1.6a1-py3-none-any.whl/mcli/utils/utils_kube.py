"""Utils for automating K8s contexts"""
# pylint: disable=too-many-lines
from __future__ import annotations

import base64
import copy
import functools
import http
import json
import logging
import math
import pydoc
import shlex
import subprocess
import threading
import time
from contextlib import contextmanager
from multiprocessing.pool import ApplyResult
from typing import (TYPE_CHECKING, Any, Callable, Dict, Generator, List, NamedTuple, Optional, Protocol, Tuple, Type,
                    Union)

from kubernetes import client, config, watch
from urllib3.response import HTTPResponse

from mcli.utils.utils_kube_labels import label
from mcli.version import Version

if TYPE_CHECKING:
    from mcli.api.model.run_model import RunStatus

logger = logging.getLogger(__name__)


def make_label_selector_from_labels(labels: Dict[str, Optional[Union[str, List[str]]]]) -> str:
    """Create a label selector string from a dictionary of labels.

    If multiple values for a label key are provided, then an 'in' set operation is used.

    Example outputs:
        mosaicml.com/job=bert-run-eyxr
        mosaicml.com/job in (bert-run-eyxr,bert-run-2-eyxr)

    Args:
        labels (Dict[str, Union[Optional[str], List[str]]]): The dictionary mapping label key to label value(s)

    Returns:
        str: The label selector as a string.
    """
    parts = []
    for key, value in labels.items():
        if isinstance(value, list):
            value_set_string = '(' + ','.join([v if v else '' for v in value]) + ')'
            part = f'{key} in {value_set_string}'
            parts.append(part)
        else:
            part = f"{key}{('=' + value) if value else ''}"
            parts.append(part)
    return ','.join(parts)


def kube_object_to_dict(obj: Any) -> Dict[str, Any]:
    """Convert an object returned by the Kubernetes API to a dict

    Args:
        obj (Kubernetes object): A Kubernetes object returned from the ``kubernetes.client``

    Returns:
        Dict[str, Any]: The serialized dictionary form of the ``obj``
    """
    api_client = client.ApiClient()
    return api_client.sanitize_for_serialization(obj)


def deserialize(obj_dict: Dict[str, Any], object_name: str) -> Any:
    """Deserialize a Kubernetes object json to the corresponding Kubernetes object

    Args:
        obj_dict: Kubernetes object dict
        object_name: Name of the desired Kubernetes object, e.g. V1Pod, V1Job, etc.

    Returns:
        The deserialized Kubernetes object
    """
    api_client = client.ApiClient()

    class FakeResponse:
        data = json.dumps(obj_dict)

    return api_client.deserialize(FakeResponse, object_name)


class KubeContext():

    def __init__(self, name: str, namespace: Optional[str] = None, **kwargs):
        del kwargs  # unused

        # K8s context objects also contain a cluster and user, but MCLI doesn't use them.

        self.name = name
        self.namespace = namespace

    def __str__(self) -> str:
        return (f'name: {self.name},'
                f" \t{'namespace: ' + self.namespace if self.namespace else ''}")


class Timer():
    """Simple timer used in event streaming

    Args:
        duration: Number of seconds to run
    """

    def __init__(self, duration: float):
        self.duration = duration
        self._start = time.time()

    @property
    def elapsed(self) -> float:
        return time.time() - self._start

    @property
    def remaining(self) -> float:
        return self.duration - self.elapsed


def robust_stream_events(api_call,
                         timeout: Optional[int] = None,
                         shutdown: Optional[threading.Event] = None,
                         **kwargs) -> Generator[Dict[str, Any], None, None]:
    """Stream Kubernetes API call events

    Args:
        api_call: API call to stream
        timeout: Optional timeout for the stream
        shutdown: Optional threading.Event used to trigger shutdown
        **kwargs: Additional keyword arguments to pass to ``api_call``

    Raises:
        RuntimeError: raised if a timeout is requested but the api_call doesn't have
        known timeout argument (``timeout_seconds`` or ``_request_timeout``)

    Yields:
        Kubernetes stream events. This is a dictionary with three keys: "type", "object"
        and "rawObject". The "type" says whether the event was an update, addition or
        deletion. The "object" tells you what the referenced object is, as a deserialized
        Kubernetes API object (e.g. V1PodList).
    """

    watcher = watch.Watch()
    watch_timeout = None
    timer: Optional[Timer] = None
    if timeout is not None:
        timer = Timer(timeout)

    if isinstance(api_call, functools.partial):
        functools.update_wrapper(api_call, api_call.func)
    sig = pydoc.getdoc(api_call)

    timeout_key: Optional[str] = None
    if ':param int timeout_seconds:' in sig:
        timeout_key = 'timeout_seconds'
    elif ':param _request_timeout:' in sig:
        timeout_key = '_request_timeout'
    elif timeout is not None:
        raise RuntimeError('Could not find an appropriate key to pass a timeout argument')

    resource_version: Optional[str] = kwargs.get('resource_version', None)
    shutdown = shutdown or threading.Event()
    while not shutdown.is_set():
        watch_timeout = 1
        if timer:
            watch_timeout = min(int(math.ceil(timer.remaining)), 1)
        if watch_timeout <= 0:
            break

        if timeout_key is not None:
            kwargs[timeout_key] = watch_timeout

        if resource_version:
            kwargs['resource_version'] = resource_version
        try:
            for event in watcher.stream(api_call, **kwargs):
                if shutdown.is_set():
                    break
                resource_version = event['object'].metadata.resource_version
                yield event
        except client.ApiException as e:
            # Catch
            if e.status == http.HTTPStatus.GONE:
                resource_version = None
                del kwargs['resource_version']
                continue
            raise
        finally:
            watcher.stop()


def robust_stream_job_events(name: str,
                             namespace: str,
                             timeout: Optional[int] = None) -> Generator[client.CoreV1Event, None, None]:
    """Stream job events for the specified job

    Args:
        name: Name of the job
        namespace: Namespace in which the job lives
        timeout: Optional timeout, in seconds, for streaming. Defaults to None.

    Yields:
        A stream of job events
    """

    api = client.CoreV1Api()
    field_selector = f'involvedObject.kind=Job,involvedObject.name={name}'
    kwargs: Dict[str, Any] = {}

    initial_events: client.CoreV1EventList = api.list_namespaced_event(namespace=namespace,
                                                                       timeout_seconds=timeout,
                                                                       field_selector=field_selector)
    resource_version: Optional[str] = None
    if initial_events:
        for event in initial_events.items:
            resource_version = event.metadata.resource_version
            yield event
    if resource_version:
        kwargs['resource_version'] = resource_version
    for event in robust_stream_events(api.list_namespaced_event,
                                      namespace=namespace,
                                      field_selector=field_selector,
                                      timeout=timeout,
                                      **kwargs):

        yield event['object']


def get_job_num_pods(name: str, namespace: str) -> int:
    """Get the number of pods a job is expected to spawn

    Args:
        name: Name of the job
        namespace: Namespace in which the job exists

    Returns:
        Number of pods expected from the job
    """
    api = client.BatchV1Api()
    k8s_job: client.V1Job = api.read_namespaced_job(name, namespace)
    return int(k8s_job.spec.parallelism or 1)


def wait_for_job_pods(name: str,
                      namespace: str,
                      num_pods: Optional[int] = None,
                      timeout: Optional[int] = 30) -> List[str]:
    """Wait for a job's pods to spawn and retun a list of pod names

    Args:
        name: Name of the job
        namespace: Namespace in which the job exists
        num_pods: Number of pods to wait for. If not provided, this will be requested. Default None.
        timeout: Optional timeout for how long to wait for pod(s) to spawn. `None` can be
            passed to disable the timeout. Default 30.

    Returns:
        List of pod names
    """

    if num_pods is None:
        num_pods = get_job_num_pods(name, namespace)

    pod_names = []
    for event in robust_stream_job_events(name, namespace, timeout):
        if event.reason == 'SuccessfulCreate':
            pod_name = event.message.replace('Created pod: ', '').strip()
            pod_names.append(pod_name)

        if len(pod_names) == num_pods:
            break
    return pod_names


def connect_to_pod(name: str, context: KubeContext) -> bool:
    """Connect to a pod for interactive use

    Note: If the kubectl command fails, the failure will be printed to stderr by the
    kubectl command and p.wait() will exit immediately.

    Args:
        name: Name of the pod
        context: Kubernetes context in which the pod lives

    Returns:
        True if connection succeeded (after connection is closed) or False if connection closed unexpectedly
    """
    # pylint: disable=import-outside-toplevel
    from mcli.config import MCLI_KUBECONFIG

    if context.namespace is None:
        raise ValueError('Context must have a valid namespace specified, not None')
    options = (f'--kubeconfig {shlex.quote(str(MCLI_KUBECONFIG))} '
               f'--context {shlex.quote(context.name)} '
               f'--namespace {shlex.quote(context.namespace)}')
    exec_command = f'kubectl exec -it {options} {name} -- /bin/bash'

    logger.debug(f'Calling: {exec_command}')
    with subprocess.Popen(exec_command, shell=True, start_new_session=True) as p:
        return p.wait() == 0


def get_kube_contexts() -> List[KubeContext]:
    """Returns all configured K8s configured contexts

    Returns:
        List[KubeContext]: A list of the k8s contexts configured.
    """
    # pylint: disable=import-outside-toplevel
    from mcli.config import MCLI_KUBECONFIG
    raw_contexts = config.list_kube_config_contexts(config_file=str(MCLI_KUBECONFIG))[0]

    contexts = [KubeContext(name=x['name'], **x['context']) for x in raw_contexts]
    return contexts


def get_current_context() -> KubeContext:
    """Returns the current K8s context

    Returns:
        KubeContext: The current K8s context
    """
    # pylint: disable=import-outside-toplevel
    from mcli.config import MCLI_KUBECONFIG
    _, current_context = config.list_kube_config_contexts(config_file=str(MCLI_KUBECONFIG))

    return KubeContext(name=current_context['name'], **current_context['context'])


# pylint: disable-next=invalid-name
def merge_V1ObjectMeta(*other: client.V1ObjectMeta) -> client.V1ObjectMeta:
    """ Merges a V1ObjectMeta into the Base V1ObjectMeta

    Does not handle lists such as `managed_fields` and `owner_references`

    Returns:
        A new V1ObjectMeta with the merged data
    """
    merged_meta = client.V1ObjectMeta()
    for attr in client.V1ObjectMeta.attribute_map:
        for o in other:
            if getattr(o, attr) is not None:
                found_attr = getattr(o, attr)
                if attr in ('labels', 'annotations') and getattr(merged_meta, attr):
                    base_labels: Dict[str, str] = getattr(merged_meta, attr)
                    base_labels.update(found_attr)
                    setattr(merged_meta, attr, base_labels)
                else:
                    setattr(merged_meta, attr, found_attr)
    return merged_meta


def safe_update_optional_list(
    original_value: Optional[List[Any]],
    additions: List[Any],
) -> List[Any]:
    """ Returns a copy with the merged optional list and additional list """
    if original_value is not None:
        return original_value + additions
    else:
        return copy.deepcopy(additions)


def safe_update_optional_dictionary(
    original_value: Optional[Dict[Any, Any]],
    additions: Dict[Any, Any],
) -> Dict[Any, Any]:
    """ Returns a copy with the merged optional dict and additional dict """
    if original_value is not None:
        new_dict = copy.deepcopy(original_value)
        new_dict.update(additions)
        return new_dict
    else:
        return copy.deepcopy(additions)


@contextmanager
def use_context(context: str) -> Generator[KubeContext, None, None]:
    """_summary_

    Args:
        context (str): Name of the context to use for Kubernetes API calls

    Raises:
        ValueError: if the requested context does not exist

    Yields:
        KubeContext: The KubeContext object for the current context
    """
    # pylint: disable=import-outside-toplevel
    from mcli.config import MCLI_KUBECONFIG
    poss_contexts = [c for c in get_kube_contexts() if c.name == context]
    if len(poss_contexts) == 0:
        raise ValueError(f'No context named {context}')
    new_context = poss_contexts[0]

    previous_context = get_current_context()
    try:
        config.load_kube_config(context=new_context.name, config_file=str(MCLI_KUBECONFIG))
        yield new_context
    finally:
        config.load_kube_config(context=previous_context.name, config_file=str(MCLI_KUBECONFIG))


def base64_encode(message: str, encoding: str = 'utf-8') -> str:
    """Encode the provided message in base64

    Args:
        message (str): Message to encode
        encoding (str, optional): Byte encoding of `message`. Defaults to "utf-8".

    Returns:
        str: base64 encoded `message`
    """
    message_bytes = message.encode(encoding)
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode(encoding)
    return base64_message


def base64_decode(base64_message: str, encoding: str = 'utf-8') -> str:
    """Decode the provided base64-encoded message

    Args:
        base64_message (str): Message encoded in base64 to decode
        encoding (str, optional): Encoding that should be used for resulting message. Defaults to "utf-8".

    Returns:
        str: Decoded message
    """
    base64_bytes = base64_message.encode(encoding)
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode(encoding)
    return message


def kube_call_idem(api_call: Callable, *args, **kwargs) -> Optional[Dict[str, Any]]:
    """Calls the requested API and returns None if the object already exists

    Args:
        api_call: A kubernetes api call
        args, kwargs: Additional *args and **kwargs for the requested API call

    Returns:
        The response if the api call succeeded or None if the object already exists

    Raises:
        Re-raises any ApiExceptions found that weren't due to the object already existing
    """

    try:
        return api_call(*args, **kwargs)
    except client.ApiException as e:
        if not (e.status == 409 and e.reason == 'Conflict'):
            # Error was not a duplicate-name conflict
            raise


def read_secret(name: str, namespace: str) -> Optional[Dict[str, Union[str, Dict[str, Any]]]]:
    """Attempt to read the requested secret

    Args:
        name (str): Name of the secret
        namespace (str): Namespace in which to look

    Returns:
        Optional[Dict[str, str]]: If None, the secret does not exist. Otherwise, the secret is returned as a JSON.
    """
    api = client.CoreV1Api()
    try:
        secret = api.read_namespaced_secret(name=name, namespace=namespace)
        return kube_object_to_dict(secret)
    except client.ApiException:
        return None


def _get_secret_spec(
    name: str,
    data: Dict[str, str],
    secret_type: str = 'Opaque',
    labels: Optional[Dict[str, str]] = None,
    annotations: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Get the Kubernetes spec for the requested secret

    Args:
        name: Name of the secret
        data: Secret data. Should be base64 encoded unless ``encode=True``.
        secret_type: Secret type. Defaults to "Opaque".
        labels: Additional labels that will be added to the secret, if provided.
        annotations: Additional annotations that will be added to the secret, if provided

    Returns:
        bool: True if creation succeeded
    """
    labels = labels or {}
    annotations = annotations or {}

    secret = client.V1Secret(type=secret_type, data=data)
    secret.metadata = client.V1ObjectMeta(name=name, labels=labels, annotations=annotations)
    return kube_object_to_dict(secret)


def create_secret(
    spec: Dict[str, Any],
    namespace: str,
) -> bool:
    """Create the requested secret

    Args:
        spec: Kubernetes spec for the secret
        namespace: Namespace in which the secret should be created

    Returns:
        bool: True if creation succeeded
    """
    api = client.CoreV1Api()
    try:
        api.create_namespaced_secret(namespace=namespace, body=spec)
    except client.ApiException:
        return False
    return True


def update_secret(
    name: str,
    namespace: str,
    data: Dict[str, str],
    labels: Optional[Dict[str, str]] = None,
    annotations: Optional[Dict[str, str]] = None,
) -> bool:
    """Update the requested secret with new data

    Args:
        name (str): Name of the secret
        namespace (str): Namespace in which the secret exists
        data (Dict[str, str]): New secret data. Should be base64 encoded unless ``encode=True``.

    Returns:
        bool: True if update succeeded
    """

    # Get existing secret
    existing_secret = read_secret(name, namespace)
    if not existing_secret:
        raise client.ApiException(f'Could not find a secret named {name} within the namespace {namespace}')
    assert existing_secret is not None
    secret_type = existing_secret['type']

    labels = labels or {}
    annotations = annotations or {}

    api = client.CoreV1Api()
    secret = client.V1Secret(type=secret_type, data=data)
    secret.metadata = client.V1ObjectMeta(name=name, labels=labels, annotations=annotations)
    api.patch_namespaced_secret(name, namespace, body=secret)
    return True


def delete_secret(name: str, namespace: str) -> bool:
    """Delete the requested secret

    Args:
        name: Name of the secret
        namespace: Namespace in which the secret exists

    Returns:
        True if deletion succeeded
    """

    api = client.CoreV1Api()
    try:
        api.delete_namespaced_secret(name, namespace)
    except client.exceptions.ApiException as e:
        logger.debug(f'Failed to delete secret {name} from namespace {namespace}')
        logger.debug(e)
        return False
    return True


def list_secrets(namespace: str, labels: Optional[Dict[str, Union[Optional[str], List[str]]]] = None) -> Dict[str, Any]:
    """List all secrets in the namespace, filtered by labels

    Args:
        namespace (str): Kubernetes namespace
        labels (Optional[Dict[str, Optional[str]]]): Secret labels that must be matched. Defaults to None.

    Returns:
        Dict[str, Any]: Kubernetes secrets list as a JSON
    """
    if labels is None:
        labels = {}
    label_selector = make_label_selector_from_labels(labels)
    api = client.CoreV1Api()
    secrets = api.list_namespaced_secret(namespace=namespace, label_selector=label_selector)
    return kube_object_to_dict(secrets)


def list_jobs(namespace: str, labels: Optional[Dict[str, Union[Optional[str], List[str]]]] = None) -> Dict[str, Any]:
    if labels is None:
        labels = {}
    label_selector = make_label_selector_from_labels(labels)
    api = client.BatchV1Api()
    jobs = api.list_namespaced_job(namespace=namespace, label_selector=label_selector)
    return kube_object_to_dict(jobs)


class ContextCall(NamedTuple):
    """A context-specific response to a Kubernetes API call
    """
    response: Dict[str, Any]
    context: KubeContext


def _async_req_all_contexts(
    contexts: List[KubeContext],
    api: Type[object],
    method_name: str,
    *args,
    **kwargs,
) -> List[ApplyResult]:
    """Call the requested method in all contexts and return async request objects

    Args:
        contexts: List of Kubernetes contexts
        api: Kubernetes API
        method_name: API method

    Returns:
        List of request objects that can be resolved with `.get()`
    """

    kwargs['async_req'] = True
    requests = []
    for context in contexts:
        if context.namespace is None:
            print(f'No namespace for context {context.name}')
            continue
        with use_context(context.name):
            kwargs['namespace'] = context.namespace
            api_client = client.ApiClient()
            context_api = api(api_client=api_client)  # type: ignore
            api_call = getattr(context_api, method_name)
            req = api_call(*args, **kwargs)
            requests.append(req)
    return requests


def multi_cluster_call(
    contexts: List[KubeContext],
    api: Type[object],
    method_name: str,
    *args,
    **kwargs,
) -> List[ContextCall]:
    """Call the requested method in all contexts

    Args:
        contexts: List of Kubernetes contexts
        api: Kubernetes API
        method_name: API method
        *args, **kwargs: Additional method arguments

    Returns:
        List ``ContextCall`` responses specifying (response, context) pairs
    """

    requests = _async_req_all_contexts(contexts, api, method_name, *args, **kwargs)
    responses = []
    for context, request in zip(contexts, requests):
        response = kube_object_to_dict(request.get())
        responses.append(ContextCall(response, context))

    return responses


class WrappedCallable(Protocol):

    def __call__(self, *args: Any, **kwargs: Any) -> List[ContextCall]:
        ...


class MultiClusterApi:
    """Wraps a Kubernetes API to asynchronously call the API in all contexts, returning a
    list of ContextCall objects

    Args:
        api: A Kubernetes API (e.g. client.CoreV1Api)
        contexts: List of Kubernetes contexts to use
    """

    def __init__(self, api: Any, contexts: List[KubeContext]):
        self.api = api
        self.contexts = contexts

    def __getattr__(self, attr: str) -> WrappedCallable:
        # Raises AttributeError if method doesn't exist
        _ = getattr(self.api, attr)
        return self._decorator(attr)

    def _decorator(self, method_name: str) -> WrappedCallable:

        def wrapper(*args, **kwargs) -> List[ContextCall]:
            return multi_cluster_call(self.contexts, self.api, method_name, *args, **kwargs)

        return wrapper


def list_pods_across_contexts(
    contexts: List[KubeContext],
    labels: Optional[Dict[str, Union[Optional[str],
                                     List[str]]]] = None) -> Tuple[List[Dict[str, Any]], List[ContextCall]]:
    """List pods across a set of contexts that match a given set of labels.

    If no labels are provided, then list all pods.

    Args:
        contexts (List[KubeContext]): The contexts to search over.
        labels (Dict[str, Optional[str]], optional): The labels to filter by.

    Returns:
        Tuple[List[Dict[str, Any]], List[ContextCall]]: A tuple containing the jobs and context call objects.
    """

    if labels is None:
        labels = {}
    label_selector = make_label_selector_from_labels(labels)
    cluster_api = MultiClusterApi(client.CoreV1Api, contexts)
    pod_responses: List[ContextCall] = cluster_api.list_namespaced_pod(label_selector=label_selector)
    all_pods = []
    for resp in pod_responses:
        all_pods.extend(resp.response['items'])
    return all_pods, pod_responses


def group_pods_by_job(pods: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Group pods by job name.

    The job name is set on each pod using the mosaic.JOB label and is equivalent to the run name.

    Args:
        pods (List[Dict[str, Any]]): The pods to group.

    Returns:
        Dict[str, List[Dict[str, Any]]]: A dictionary mapping job name to the list of pods
            associated with that job.
    """

    grouping = {}
    for p in pods:
        labels = p['metadata'].get('labels', {})
        job_name = labels.get(label.mosaic.JOB, '-')
        if job_name not in grouping:
            grouping[job_name] = []
        grouping[job_name].append(p)
    return grouping


def get_run_status_from_pod(pod: Dict[str, Any]) -> RunStatus:
    """Convert Pod status to RunStatus.

    Args:
        pod (Dict[str, Any]): The kubernetes Pod object.

    Returns:
        RunStatus: The RunStatus corresponding to the Pod phase.
    """
    # pylint: disable-next=import-outside-toplevel
    from mcli.api.model.run_model import RunStatus

    status = pod.get('status', {}).get('phase', '')
    run_status = RunStatus.UNKNOWN
    if status == 'Pending':
        run_status = RunStatus.QUEUED
    elif status == 'Running':
        run_status = RunStatus.RUNNING
    elif status == 'Succeeded':
        run_status = RunStatus.SUCCEEDED
    elif status == 'Failed':
        run_status = RunStatus.FAILED
    return run_status


def list_jobs_across_contexts(
    contexts: List[KubeContext],
    labels: Optional[Dict[str, Union[Optional[str],
                                     List[str]]]] = None) -> Tuple[List[Dict[str, Any]], List[ContextCall]]:
    """List jobs across a set of contexts that match a given set of labels.

    If no labels are provided, then list all jobs.

    Args:
        contexts (List[KubeContext]): The contexts to search over.
        labels (Dict[str, Optional[str]], optional): The labels to filter by.

    Returns:
        Tuple[List[Dict[str, Any]], List[ContextCall]]: A tuple containing the jobs and context call objects.
    """

    if labels is None:
        labels = {}
    label_selector = make_label_selector_from_labels(labels)
    cluster_api = MultiClusterApi(client.BatchV1Api, contexts)
    job_responses: List[ContextCall] = cluster_api.list_namespaced_job(label_selector=label_selector)
    all_jobs = []
    for resp in job_responses:
        all_jobs.extend(resp.response['items'])
    return all_jobs, job_responses


def list_config_maps_across_contexts(
    contexts: List[KubeContext],
    labels: Optional[Dict[str, Union[Optional[str],
                                     List[str]]]] = None) -> Tuple[List[Dict[str, Any]], List[ContextCall]]:
    """List config maps across a set of contexts that match a given set of labels.

    If no labels are provided, then list all config maps.

    Args:
        contexts (List[KubeContext]): The contexts to search over.
        labels (Dict[str, Optional[str]], optional): The labels to filter by.

    Returns:
        Tuple[List[Dict[str, Any]], List[ContextCall]]: A tuple containing the configmaps and context call objects.
    """

    if labels is None:
        labels = {}
    label_selector = make_label_selector_from_labels(labels)
    cluster_api = MultiClusterApi(client.CoreV1Api, contexts)
    config_map_responses: List[ContextCall] = cluster_api.list_namespaced_config_map(label_selector=label_selector)
    all_config_maps = []
    for resp in config_map_responses:
        all_config_maps.extend(resp.response['items'])
    return all_config_maps, config_map_responses


def list_services_across_contexts(
    contexts: List[KubeContext],
    labels: Optional[Dict[str, Union[Optional[str],
                                     List[str]]]] = None) -> Tuple[List[Dict[str, Any]], List[ContextCall]]:
    """List services across a set of contexts that match a given set of labels.

    If no labels are provided, then list all services.

    Args:
        contexts (List[KubeContext]): The contexts to search over.
        labels (Dict[str, Optional[str]], optional): The labels to filter by.

    Returns:
        Tuple[List[Dict[str, Any]], List[ContextCall]]: A tuple containing the services and context call objects.
    """

    if labels is None:
        labels = {}
    label_selector = make_label_selector_from_labels(labels)
    cluster_api = MultiClusterApi(client.CoreV1Api, contexts)
    service_responses: List[ContextCall] = cluster_api.list_namespaced_service(label_selector=label_selector)
    all_services = []
    for resp in service_responses:
        all_services.extend(resp.response['items'])
    return all_services, service_responses


def delete_job(name: str, namespace: str) -> bool:
    """Delete the requested job and the associated pods.

    Args:
        name: Name of the job
        namespace: Namespace in which the job exists

    Returns:
        True if deletion succeeded
    """

    api = client.BatchV1Api()
    try:
        api.delete_namespaced_job(name, namespace, propagation_policy='Foreground')
    except client.ApiException as e:
        logger.debug(f'Failed to delete job {name} from namespace {namespace}')
        logger.error(e)
        return False
    return True


def delete_jobs_across_contexts(contexts: List[KubeContext],
                                labels: Optional[Dict[str, Union[Optional[str], List[str]]]] = None) -> bool:
    """Delete the requested job and the associated pods across contexts.

    Args:
        contexts (List[KubeContext]): The contexts to search over.
        labels (Dict[str, Optional[str], List[str]], optional): The labels to filter by.

    Returns:
        True if deletion succeeded
    """
    if labels is None:
        labels = {}
    label_selector = make_label_selector_from_labels(labels)
    cluster_api = MultiClusterApi(client.BatchV1Api, contexts)
    responses: List[ContextCall] = cluster_api.delete_collection_namespaced_job(label_selector=label_selector,
                                                                                propagation_policy='Foreground')
    for resp in responses:
        if resp.response.get('status', '') == 'Failure':
            logger.error(resp.response.get('reason', ''))
            return False
    return True


def delete_config_map(name: str, namespace: str) -> bool:
    """Delete the requested config map

    Args:
        name: Name of the config map
        namespace: Namespace in which the config map exists

    Returns:
        True if deletion succeeded
    """
    api = client.CoreV1Api()
    try:
        api.delete_namespaced_config_map(name, namespace)
    except client.ApiException as e:
        logger.debug(f'Failed to delete config map {name} from namespace {namespace}')
        logger.debug(e)
        return False
    return True


def delete_config_maps_across_contexts(contexts: List[KubeContext],
                                       labels: Optional[Dict[str, Union[Optional[str], List[str]]]] = None) -> bool:
    """Delete the requested config maps across contexts.

    Args:
        contexts (List[KubeContext]): The contexts to search over.
        labels (Dict[str, Optional[str], List[str]], optional): The labels to filter by.

    Returns:
        True if deletion succeeded
    """
    if labels is None:
        labels = {}
    label_selector = make_label_selector_from_labels(labels)
    cluster_api = MultiClusterApi(client.CoreV1Api, contexts)
    responses: List[ContextCall] = cluster_api.delete_collection_namespaced_config_map(label_selector=label_selector)
    for resp in responses:
        if resp.response.get('status', '') == 'Failure':
            logger.error(resp.response.get('reason', ''))
            return False
    return True


def delete_service(name: str, namespace: str) -> bool:
    """Delete the requested service

    Args:
        name: Name of the service
        namespace: Namespace in which the service exists

    Returns:
        True if deletion succeeded
    """

    api = client.CoreV1Api()
    try:
        api.delete_namespaced_service(name, namespace)
    except client.ApiException as e:
        logger.debug(f'Failed to delete service {name} from namespace {namespace}')
        logger.debug(e)
        return False
    return True


def delete_services_across_contexts(contexts: List[KubeContext],
                                    labels: Optional[Dict[str, Union[Optional[str], List[str]]]] = None) -> bool:
    """Delete the requested services across contexts.

    Args:
        contexts (List[KubeContext]): The contexts to search over.
        labels (Dict[str, Optional[str], List[str]], optional): The labels to filter by.

    Returns:
        True if deletion succeeded
    """

    if labels is None:
        labels = {}

    # Need to list services and then delete because
    # delete_collection_namespaced_service is not supported in Kubernetes
    # See: https://github.com/kubernetes/client-go/issues/409 for more details

    services_to_delete, _ = list_services_across_contexts(contexts, labels)
    responses: List[ApplyResult] = []
    for c in contexts:
        with use_context(c.name):
            api = client.CoreV1Api()
            for service in services_to_delete:
                name = service.get('metadata', {}).get('name', None)
                if not name:
                    raise RuntimeError('Service object is missing a name:', service)
                if not c.namespace:
                    raise RuntimeError(f'Context {c.name} must have a specified namespace')
                res: ApplyResult = api.delete_namespaced_service(name, c.namespace, async_req=True)
                responses.append(res)
    try:
        _ = [res.get() for res in responses]
    except client.ApiException as e:
        logger.error(e)
        return False
    return True


def read_pod_logs(name: str, namespace: str) -> str:
    """Read a pod's logs

    Args:
        name: Name of the pod
        namespace: Namespace in which the pod lives

    Returns:
        The full pod logs
    """
    v1 = client.CoreV1Api()
    logs = v1.read_namespaced_pod_log(name=name, namespace=namespace)
    return logs


def get_rank0_pod(job_name: str, namespace: str) -> str:
    """Get the rank 0 pod for the specified job

    Utilizes the pod's "completion index" annotation to get the rank 0 pod for the
    specified job. If the first pod discovered lacks this annotation, then it is
    considered rank 0. If the rank 0 pod does not exist, somehow, a RuntimeError is raised.

    Args:
        job_name: Name of the job
        namespace: Namespace in which the job lives

    Returns:
        Name of the rank 0 pod
    """
    api = client.CoreV1Api()
    pods: client.V1PodList = api.list_namespaced_pod(namespace=namespace,
                                                     label_selector=make_label_selector_from_labels(
                                                         {'job-name': job_name}))

    for pod in pods.items:
        annotations = pod.metadata.annotations
        if annotations:
            rank = int(annotations.get(label.kube_batch.POD_RANK, '0'))
        else:
            rank = 0
        if rank == 0:
            return pod.metadata.name
    raise RuntimeError(f'Could not find a rank 0 pod for job: {job_name}')


def stream_pod_logs(name: str, namespace: str) -> Generator[str, None, None]:
    """Generator for a pod's logs

    Args:
        name: Name of the pod
        namespace: Namespace in which the pod lives

    Yields:
        Line of log text
    """
    v1 = client.CoreV1Api()
    resp: HTTPResponse = v1.read_namespaced_pod_log(name=name, namespace=namespace, follow=True, _preload_content=False)
    prev_bytes = b''
    prev = ''
    for byte_str in resp.stream(amt=None, decode_content=False):
        byte_str = prev_bytes + byte_str
        try:
            decoded = byte_str.decode('utf8')
            prev_bytes = b''
        except UnicodeDecodeError as e:
            prev_bytes = byte_str[e.start:]
            decoded = byte_str[:e.start].decode('utf8')
        decoded, prev = prev + decoded, ''

        lines = decoded.split('\n')
        if not decoded.endswith('\n'):
            prev = lines.pop()
        for line in lines:
            if line:
                yield line
    if prev:
        yield prev


def find_pods_by_label(contexts: List[KubeContext], labels: Dict[str, str]) -> Optional[ContextCall]:
    """Find a set of pods by label and return the first context has them

    Args:
        contexts: List of contexts in which the pods might live
        labels: Labels to filter on

    Returns:
        ContextCall tuple with (response, context) pair. If a list of pods was found,
        the `response` attribute will have an 'items' key with a list of pod specs. If no
        pods were found, None is returned.
    """
    label_selector = ','.join([f"{key}{('=' + value) if value else ''}" for key, value in labels.items()])
    api = MultiClusterApi(client.CoreV1Api, contexts)
    responses: List[ContextCall] = api.list_namespaced_pod(label_selector=label_selector)
    for resp in responses:
        if resp.response['items']:
            return resp


class PlatformRun(NamedTuple):
    name: str
    context: KubeContext


def delete_runs(runs: List[PlatformRun], check_only_job: bool = True, wait: bool = True):
    job_responses: Dict[str, List[Optional[ApplyResult]]] = {}
    for run in runs:
        with use_context(run.context.name):
            batch = client.BatchV1Api()
            core = client.CoreV1Api()
            try:
                job_responses[run.name] = []
                job_responses[run.name].append(
                    batch.delete_namespaced_job(
                        run.name,
                        run.context.namespace,
                        async_req=True,
                        propagation_policy='Foreground',
                    ))
                job_responses[run.name].append(
                    core.delete_namespaced_config_map(
                        run.name,
                        run.context.namespace,
                        async_req=True,
                    ))
                job_responses[run.name].append(
                    core.delete_namespaced_service(
                        run.name,
                        run.context.namespace,
                        async_req=True,
                    ))

            except client.ApiException:
                job_responses[run.name] = [None]

    success: Dict[str, List[bool]] = {}
    if wait:
        for name, responses in job_responses.items():
            success[name] = []
            if check_only_job:
                responses = responses[:1]
            for response in responses:
                if response is None:
                    success[name].append(False)
                    break
                else:
                    success[name].append(response.get().status == 'Success')
    else:
        success = {
            name: [True] * len(responses) if responses[0] is not None else [False]
            for name, responses in job_responses.items()
        }


def get_cluster_version() -> Version:
    """Get the Kubernetes version for the current cluster

    Returns:
        Version tuple for the cluster Kubernetes version
    """

    version_api = client.VersionApi()
    version_info: client.VersionInfo = version_api.get_code()
    major = int(version_info.major)
    minor = int(version_info.minor)
    server_version = Version(major, minor, 0)
    return server_version
