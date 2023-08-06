"""mcli logs entrypoint"""
import argparse
import logging
import sys
from typing import Iterator, List, Optional, Tuple

from kubernetes import client

from mcli.config import MESSAGE, MCLIConfig, MCLIConfigError
from mcli.models.mcli_platform import MCLIPlatform
from mcli.utils.utils_epilog import CommonLog, ContextPodStatus, EpilogSpinner, RunEpilog
from mcli.utils.utils_kube import deserialize, find_pods_by_label, read_pod_logs, stream_pod_logs
from mcli.utils.utils_kube_labels import label
from mcli.utils.utils_logging import FAIL, INFO, console
from mcli.utils.utils_pod_state import PodState

logger = logging.getLogger(__name__)


def find_pods_and_platform(run_name: str) -> Tuple[List[client.V1Pod], MCLIPlatform]:
    """Find the pods for a given run and the platform in which it exists
    """
    conf = MCLIConfig.load_config()
    all_contexts = [platform.to_kube_context() for platform in conf.platforms]
    with console.status('Requesting run logs...'):
        context_pods = find_pods_by_label(all_contexts, {label.mosaic.JOB: run_name})
        if not context_pods:
            raise RuntimeError(f'Could not find run: {run_name}')
        platform = MCLIPlatform.from_kube_context(context_pods.context, context_pods.context.name)
        pods = [deserialize(pod_dict, 'V1Pod') for pod_dict in context_pods.response['items']]
    return pods, platform


def get_logs(run_name: str, rank: int = 0, follow: bool = True, **kwargs) -> int:
    del kwargs

    try:
        pods, platform = find_pods_and_platform(run_name)
        statuses = [ContextPodStatus.from_pod(pod) for pod in pods]

        pod: Optional[client.V1Pod] = None
        context_status: Optional[ContextPodStatus] = None
        for pod, context_status in zip(pods, statuses):
            if context_status.rank == rank:
                break
        else:
            raise RuntimeError(f'Could not find the rank {rank} instance for run {run_name}')

        # Pylint help. RuntimeError will raise if these did not get values
        assert pod is not None
        assert context_status is not None

        status = context_status.status
        with MCLIPlatform.use(platform):
            TIMEOUT = 300  # pylint: disable=invalid-name
            if follow and status.state.after(PodState.QUEUED) and status.state.before(PodState.RUNNING):
                # Pod is creating, so let's use an epilog
                logger.info(f'{INFO} Waiting for run to start, press Ctrl+C to quit')
                epilog = RunEpilog(run_name, platform.namespace)
                with EpilogSpinner() as spinner:
                    status = epilog.wait_until(callback=spinner, timeout=TIMEOUT)

            if status is None:
                # Pod epilog timed out
                logger.info(f'{INFO} Run {run_name} did not start within {TIMEOUT} seconds. Try again later.')
                return 0
            elif status.state == PodState.FAILED_PULL:
                # Pod failed at image pull so no logs present
                CommonLog(logger).log_pod_failed_pull(run_name, pod.containers[0].image)
                return 1
            elif status.state.before(PodState.QUEUED, inclusive=True):
                # Pod still waiting to be scheduled. Return
                logger.info(f'{INFO} Run {run_name} has not been scheduled')
                return 0
            elif status.state.before(PodState.RUNNING):
                # Pod still not running, probably because follow==False
                logger.info(f'{INFO} Run has not yet started. You can check the status with `mcli get runs` '
                            'and try again later.')
                return 0

            log_stream: Iterator[str]
            if follow:
                log_stream = stream_pod_logs(pod.metadata.name, platform.namespace)
            else:
                log_stream = iter(read_pod_logs(pod.metadata.name, platform.namespace).splitlines())

            for line in log_stream:
                print(line, file=sys.stdout)

    except RuntimeError as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
        return 1
    return 0


def configure_argparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.set_defaults(func=get_logs)
    parser.add_argument('run_name', metavar='RUN', help='The name of the run')
    parser.add_argument('--rank',
                        type=int,
                        default=0,
                        metavar='N',
                        help='Rank of the node in a multi-node run whose logs you\'d like to view')
    follow_grp = parser.add_mutually_exclusive_group()
    follow_grp.add_argument('--no-follow',
                            action='store_false',
                            dest='follow',
                            help='Do not follow the logs of an in-progress run. '
                            'Simply print any existing logs and exit')
    follow_grp.add_argument('-f',
                            '--follow',
                            action='store_true',
                            dest='follow',
                            help='Follow the logs of an in-progress run. This is the default behavior')

    return parser


def add_log_parser(subparser: argparse._SubParsersAction):
    """Add the parser for retrieving run logs
    """

    # pylint: disable=invalid-name
    EXAMPLES = """

Examples:

# Follow the logs of an ongoing run
> mcli logs run-1234

# Follow the logs of a specific node in a multinode run
> mcli logs multinode-run-1234 --rank 1

# Print only the logs up until this point for an ongoing run
> mcli logs run-1234 --no-follow
"""

    log_parser: argparse.ArgumentParser = subparser.add_parser(
        'logs',
        aliases=['log'],
        help='View the logs from a specific run',
        description='View the logs of an ongoing, completed or failed run',
        epilog=EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    log_parser = configure_argparser(log_parser)

    return log_parser
