""" m delete Entrypoint """
import argparse
from typing import List, Optional

from mcli.api.model.run_model import RunStatus
from mcli.cli.m_delete.delete import delete_environment_variable, delete_platform, delete_run, delete_secret


def delete(parser, **kwargs) -> int:
    del kwargs
    parser.print_help()
    return 0


def add_common_args(parser: argparse.ArgumentParser):
    parser.add_argument('-y',
                        '--force',
                        dest='force',
                        action='store_true',
                        help='Skip confirmation dialog before deleting. Please be careful!')


def configure_argparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    subparsers = parser.add_subparsers()
    parser.set_defaults(func=delete, parser=parser)

    # TODO: Delete Projects

    platform_parser = subparsers.add_parser(
        'platform',
        aliases=['platforms'],
        help='Delete a Platform',
    )
    platform_parser.add_argument('platform_name', help='The name of the platform to delete')
    platform_parser.set_defaults(func=delete_platform)
    add_common_args(platform_parser)

    environment_parser = subparsers.add_parser(
        'env',
        aliases=['environment-variable'],
        help='Delete an Environment Variable',
    )
    environment_parser.add_argument('variable_name', help='The name of the environment variable to delete')
    environment_parser.set_defaults(func=delete_environment_variable)
    add_common_args(environment_parser)

    secrets_parser = subparsers.add_parser(
        'secrets',
        aliases=['secret'],
        help='Delete a Secret',
    )
    secrets_parser.add_argument('secret_name', help='The name of the secret to delete')
    secrets_parser.set_defaults(func=delete_secret)
    add_common_args(secrets_parser)

    run_parser = subparsers.add_parser(
        'run',
        aliases=['runs'],
        help='Delete a Run',
    )
    run_parser.add_argument('-n',
                            '--name',
                            nargs='+',
                            dest='name_filter',
                            default=None,
                            help='The name of the run to delete')
    run_parser.add_argument('-p',
                            '--platform',
                            nargs='+',
                            dest='platform_filter',
                            default=None,
                            help='The platforms to delete all runs on')
    run_parser.add_argument('-s',
                            '--status',
                            dest='status_filter',
                            nargs='+',
                            default=None,
                            choices=[
                                RunStatus.QUEUED.value, RunStatus.RUNNING.value, RunStatus.FAILED.value,
                                RunStatus.SUCCEEDED.value, RunStatus.UNKNOWN.value
                            ],
                            help='Delete runs with the specified statuses')
    run_parser.add_argument('-a', '--all', dest='delete_all', action='store_true', help='Delete all runs')
    run_parser.set_defaults(func=delete_run)
    add_common_args(run_parser)

    return parser


def add_delete_argparser(subparser: argparse._SubParsersAction,
                         parents: Optional[List[argparse.ArgumentParser]] = None) -> argparse.ArgumentParser:
    del parents
    delete_parser: argparse.ArgumentParser = subparser.add_parser(
        'delete',
        aliases=['del'],
        help='Configure your local project',
    )
    delete_parser = configure_argparser(parser=delete_parser)
    return delete_parser
