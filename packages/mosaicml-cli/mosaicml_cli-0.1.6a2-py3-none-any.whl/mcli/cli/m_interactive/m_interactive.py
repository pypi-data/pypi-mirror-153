""" mcli interactive Entrypoint """
import argparse
import logging
from typing import Dict, Optional, Set

from mcli.config import MESSAGE, MCLIConfig, MCLIConfigError
from mcli.models.mcli_platform import MCLIPlatform
from mcli.models.run_input import PartialRunInput, RunInput
from mcli.serverside.job.mcli_job import MCLIJob, MCLIJobType
from mcli.serverside.platforms.instance_type import GPUType
from mcli.serverside.platforms.platform import GenericK8sPlatform
from mcli.serverside.runners.runner import Runner
from mcli.utils.utils_epilog import CommonLog, EpilogSpinner, RunEpilog
from mcli.utils.utils_interactive import query_yes_no
from mcli.utils.utils_kube import PlatformRun, connect_to_pod, delete_runs
from mcli.utils.utils_logging import FAIL, INFO, OK, console
from mcli.utils.utils_pod_state import PodState, PodStatus
from mcli.utils.utils_types import get_hours_type

_MAX_INTERACTIVE_DURATION: float = 12

logger = logging.getLogger(__name__)


def get_interactive_platform(platform_str: Optional[str] = None) -> GenericK8sPlatform:
    """Gets an interactive-enabled platform

    If ``platform_str`` is not ``None``, then the corresponding Kubernetes platform is returned
    if it has interactive enabled. If not, it errors with a ``RuntimeError``. If ``platform_str``
    is ``None``, all possible interactive platforms are detected. If none exist, then a
    ``RuntimeError`` is thrown. If more than one exist, the user is prompted to choose one.

    Args:
        platform_str: Optional name of the platform on which to run the session. Defaults to None.

    Returns:
        A valid Kubernetes platform

    Raises:
        RuntimeError: Raised if a valid Kubernetes platform could not be found.
    """
    interactive_platforms: Dict[str, GenericK8sPlatform] = {}
    mcli_platform: Optional[MCLIPlatform] = None
    for pl in MCLIConfig.load_config(safe=True).platforms:
        if pl.name == platform_str:
            mcli_platform = pl
        k8s_platform = GenericK8sPlatform.from_mcli_platform(pl)
        if k8s_platform.interactive:
            interactive_platforms[pl.name] = k8s_platform

    if platform_str is not None:
        if mcli_platform is not None and (mcli_platform.name not in interactive_platforms):
            raise RuntimeError(f'Platform {platform_str} does not permit interactive sessions')
        assert mcli_platform is not None
        return interactive_platforms[mcli_platform.name]

    if not interactive_platforms:
        raise RuntimeError('None of your configured platforms permit interactive sessions. If you should have access '
                           'to one, make sure to create it using `mcli create platform`.')

    valid_mcli_platforms = list(interactive_platforms.keys())
    if len(valid_mcli_platforms) > 1:
        if 'r1z2' in valid_mcli_platforms:
            chosen_platform = 'r1z2'
        else:
            raise RuntimeError('Multiple platforms found that permit interactive sessions. Please specify one of '
                               f'{valid_mcli_platforms} with the --platform argument.')
    else:
        chosen_platform = valid_mcli_platforms[0]

    return interactive_platforms[chosen_platform]


def get_interactive_instances_available() -> Dict[GPUType, Set[int]]:
    available: Dict[GPUType, Set[int]] = {}

    for pl in MCLIConfig.load_config(safe=True).platforms:
        k8s_platform = GenericK8sPlatform.from_mcli_platform(pl)
        if k8s_platform.interactive:
            for gpu_type, gpu_nums in k8s_platform.allowed_instances.available_instances.items():
                if gpu_type not in available:
                    available[gpu_type] = set()
                available[gpu_type].update(gpu_nums)
    return available


def interactive_entrypoint(
    name: Optional[str] = None,
    gpu_type: Optional[GPUType] = GPUType.NONE,
    gpu_num: int = 1,
    cpus: int = 1,
    platform: Optional[str] = None,
    hours: float = 1,
    image: str = 'mosaicml/pytorch',
    confirm: bool = True,
    connect: bool = True,
    **kwargs,
) -> int:
    del kwargs
    if gpu_type is None:
        gpu_type = GPUType.NONE

    try:
        chosen_platform = get_interactive_platform(platform)
        instance = chosen_platform.get_instance_type(gpu_type, gpu_num, cpus)
        if not name:
            name = f'interactive-{instance.gpu_type.value.replace("_", "-")}-{instance.gpu_num}'.lower()

        partial_run = PartialRunInput(
            run_name=name,
            platform=chosen_platform.mcli_platform.name,
            gpu_type=gpu_type.value,
            gpu_num=gpu_num,
            cpus=cpus,
            command=f'sleep {int(3600 * hours)}',
            image=image,
        )
        run_input = RunInput.from_partial_run_input(partial_run)

        mcli_job = MCLIJob.from_run_input(run_input=run_input)

        gpu_cpu_string = f'{gpu_num} GPU(s)' if gpu_type != GPUType.NONE else f'{cpus} CPU(s)'
        logger.info(
            f'{OK} Ready to submit a [bold]{gpu_cpu_string}[/] interactive session for [bold]{hours} hour(s)[/] '
            f'to platform [bold green]{chosen_platform.mcli_platform.name}[/]')
        if confirm:
            confirm = query_yes_no('Do you want to submit?')
            if not confirm:
                raise RuntimeError('Canceling!')

        exit_code = run_mcli_job_interactively(mcli_job, chosen_platform.mcli_platform, connect)
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
        return 1
    except RuntimeError as e:
        logger.error(e)
        return 1

    return exit_code or 0


def run_mcli_job_interactively(
    mcli_job: MCLIJob,
    mcli_platform: MCLIPlatform,
    connect: bool,
) -> int:
    runner = Runner()
    runner.submit(job=mcli_job, job_type=MCLIJobType.INTERACTIVE)
    if connect:
        with MCLIPlatform.use(mcli_platform):
            logger.info(f'{INFO} Interactive session submitted. Waiting for it to start...')
            logger.info(f'{INFO} Press Ctrl+C to quit and interact with your session manually.')
            epilog = RunEpilog(mcli_job.unique_name, mcli_platform.namespace)
            last_status: Optional[PodStatus] = None
            with EpilogSpinner() as spinner:
                last_status = epilog.wait_until(callback=spinner, timeout=300)

            # Wait timed out
            common_log = CommonLog(logger)
            context = mcli_platform.to_kube_context()
            exec_cmd = f'kubectl --context {context.name} exec -it {epilog.rank0_pod} -- /bin/bash'
            if last_status is None:
                get_pods_cmd = f'kubectl --context {context.name} get pods -w {epilog.rank0_pod}'
                logger.warning(
                    'Waiting for interactive session to spawn exceeded the timeout. You can monitor it '
                    f'using:\n\n{get_pods_cmd}\n\n'
                    f'Once the pod is "Running", you can attach to it using:\n\n{exec_cmd}',)
                return 0
            elif last_status.state == PodState.FAILED_PULL:
                common_log.log_pod_failed_pull(mcli_job.unique_name, mcli_job.image)
                with console.status('Deleting failed run...'):
                    delete_runs([PlatformRun(mcli_job.unique_name, mcli_platform.to_kube_context())])
                return 1
            elif last_status.state == PodState.FAILED:
                common_log.log_pod_failed(mcli_job.unique_name)
                return 1
            elif last_status.state.before(PodState.RUNNING):
                common_log.log_unknown_did_not_start()
                logger.debug(last_status)
                return 1

            logger.info(f'{OK} Interactive session created. Attaching...')
            logger.info(
                f'{INFO} Press Ctrl+C to quit attaching. Once attached, press Ctrl+D or type exit '
                'to leave the session.',)
            connected = connect_to_pod(epilog.rank0_pod, context)
            if not connected:
                logger.warning(f'{FAIL} Could not connect to the interactive session.')
                logger.warning(
                    f'Please double-check that [bold]{context.name}[/] is your context and '
                    f'[bold]{context.namespace}[/] is your correct namespace.',)
                logger.warning(f'If so, try manually running {exec_cmd}')
    else:
        logger.info(f'{OK} Interactive session submitted. Please use `kubectl` to connect to it')
    return 0


def configure_argparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    available_instances = get_interactive_instances_available()
    interactive_instance_numbers: Set[int] = set()
    interactive_instance_gpu_types: Set[GPUType] = set()
    for gpu_type, gpu_num in available_instances.items():
        interactive_instance_gpu_types.add(gpu_type)
        interactive_instance_numbers.update(gpu_num)
    gpu_nums = sorted(list(interactive_instance_numbers))
    gpu_types = sorted([x for x in interactive_instance_gpu_types if x.value != 'none'])
    gpu_types.insert(0, GPUType.NONE)
    gpu_default = 'a100_40gb' if 'a100_40gb' in gpu_types else 'none'

    parser.add_argument(
        '--name',
        default=None,
        type=str,
        help='Name for the interactive session. '
        'Default: "interactive-<gpu type>-<gpu num>"',
    )
    parser.add_argument(
        '--gpu-type',
        type=GPUType.from_string,
        choices=gpu_types,
        default=gpu_default,
        help='Number of GPUs to run interactively. '
        f'Default: %(default)s.  Choices: {", ".join([str(x) for x in gpu_types])}',
    )
    parser.add_argument(
        '--gpu-num',
        default=1,
        type=int,
        choices=gpu_nums,
        help='Number of GPUs to run interactively. Available numbers depend on the gpu-type chosen. '
        f'Default: %(default)s.  Choices: {", ".join([str(x) for x in gpu_nums])}',
    )
    parser.add_argument(
        '--cpus',
        default=1,
        type=int,
        help='Number of CPUs to run interactively. Must be used with <gpu type> None. '
        'Default: %(default)s',
    )
    parser.add_argument(
        '--platform',
        default=None,
        help='Platform where your interactive session should run. If you '
        'only have one available, that one will be selected by default',
    )
    parser.add_argument(
        '--hours',
        default=1,
        type=get_hours_type(_MAX_INTERACTIVE_DURATION),
        help='Number of hours the interactive session should run. '
        f' Default: %(default)s. MAX: {_MAX_INTERACTIVE_DURATION}',
    )
    parser.add_argument(
        '--image',
        default='mosaicml/pytorch',
        help='Docker image to use',
    )
    parser.add_argument(
        '-y',
        '--no-confirm',
        dest='confirm',
        action='store_false',
        help='Do not request confirmation',
    )
    parser.add_argument(
        '--no-connect',
        dest='connect',
        action='store_false',
        help='Do not connect to the interactive session immediately',
    )

    parser.set_defaults(func=interactive_entrypoint)
    return parser


def add_interactive_argparser(subparser: argparse._SubParsersAction,) -> argparse.ArgumentParser:
    """Adds the get parser to a subparser

    Args:
        subparser: the Subparser to add the Get parser to
    """

    interactive_parser: argparse.ArgumentParser = subparser.add_parser(
        'interactive',
        aliases=['int'],
        help='Get an interactive instance',
    )
    get_parser = configure_argparser(parser=interactive_parser)
    return get_parser
