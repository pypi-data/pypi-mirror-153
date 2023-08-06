""" mcli run Entrypoint """
import argparse
import logging
import textwrap
from typing import List, Optional

from mcli import config
from mcli.api.model.run_model import RunModel
from mcli.models import PartialRunInput, RunInput
from mcli.models.mcli_platform import MCLIPlatform
from mcli.serverside.job.mcli_job import MCLIJob
from mcli.serverside.platforms.experimental import ExperimentalFlag
from mcli.serverside.platforms.platform import PriorityLabel
from mcli.serverside.runners.runner import Runner
from mcli.utils.utils_epilog import CommonLog, EpilogSpinner, RunEpilog
from mcli.utils.utils_kube import PlatformRun, delete_runs, stream_pod_logs
from mcli.utils.utils_logging import FAIL, INFO, OK, console
from mcli.utils.utils_pod_state import PodState, PodStatus

logger = logging.getLogger(__name__)


def run_entrypoint(
    file: str,
    experimental: Optional[List[ExperimentalFlag]] = None,
    priority: Optional[PriorityLabel] = None,
    tail: bool = True,
    **kwargs,
) -> int:
    del kwargs
    # TODO: Reintroduce experimental
    del experimental
    logger.info(
        textwrap.dedent("""
    ------------------------------------------------------
    Let's run this run
    ------------------------------------------------------
    """))

    partial_run_input = PartialRunInput.from_file(path=file)
    run_input = RunInput.from_partial_run_input(partial_run_input)
    mcli_job = run(run_input=run_input, priority=priority)

    if tail:
        with MCLIPlatform.use(mcli_job.platform.mcli_platform) as platform:
            logger.info(f'{INFO} Run {mcli_job.unique_name} submitted. Waiting for it to start...')
            logger.info(f'{INFO} Press Ctrl+C to quit and follow your run manually.')
            epilog = RunEpilog(mcli_job.unique_name, platform.namespace)
            last_status: Optional[PodStatus] = None
            with EpilogSpinner() as spinner:
                last_status = epilog.wait_until(callback=spinner, timeout=300)

            # Wait timed out
            common_log = CommonLog(logger)
            if last_status is None:
                common_log.log_timeout()
                return 0
            elif last_status.state == PodState.FAILED_PULL:
                common_log.log_pod_failed_pull(mcli_job.unique_name, mcli_job.image)
                with console.status('Deleting failed run...'):
                    delete_runs([PlatformRun(mcli_job.unique_name, platform.to_kube_context())])
                return 1
            elif last_status.state == PodState.FAILED:
                common_log.log_pod_failed(mcli_job.unique_name)
                return 1
            elif last_status.state.before(PodState.RUNNING):
                common_log.log_unknown_did_not_start()
                logger.debug(last_status)
                return 1

            logger.info(f'{OK} Run {mcli_job.run_name} started')
            logger.info(f'{INFO} Following run logs. Press Ctrl+C to quit.\n')
            for line in stream_pod_logs(epilog.rank0_pod, platform.namespace):
                print(line)
    return 0


def run(run_input: RunInput, priority: Optional[PriorityLabel] = None) -> MCLIJob:
    if config.feature_enabled(config.FeatureFlag.USE_FEATUREDB):
        run_model = RunModel.from_run_input(run_input=run_input)
        # pylint: disable-next=import-outside-toplevel
        from mcli.api.runs.create_run import create_run
        if not create_run(run_model):
            logger.warning(f'{FAIL} Failed to persist run')

    # Populates the full MCLI Job including user defaults
    mcli_job = MCLIJob.from_run_input(run_input=run_input)

    runner = Runner()
    priority_class = priority.value if priority else None
    runner.submit(job=mcli_job, priority_class=priority_class)
    return mcli_job


def add_run_argparser(subparser: argparse._SubParsersAction) -> None:
    run_parser: argparse.ArgumentParser = subparser.add_parser(
        'run',
        aliases=['r'],
        help='Run stuff',
    )
    run_parser.set_defaults(func=run_entrypoint)
    _configure_parser(run_parser)


def _configure_parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        '-f',
        '--file',
        dest='file',
        help='File from which to load arguments.',
    )

    parser.add_argument(
        '--experimental',
        choices=ExperimentalFlag.permitted(),
        type=ExperimentalFlag,
        nargs='+',
        default=None,
        metavar='FLAG',
        help=
        'Enable one or more experimental flags. These flags are designed to take advantage of a specific feature that '
        'may still be too experimental for long-term inclusion in mcli.',
    )

    parser.add_argument(
        '--priority',
        choices=list(PriorityLabel),
        type=PriorityLabel.ensure_enum,
        help='Priority level at which runs should be submitted. '
        '(default None)',
    )

    parser.add_argument(
        '--no-tail',
        action='store_false',
        dest='tail',
        help='Do not automatically try to follow the run\'s logs',
    )
