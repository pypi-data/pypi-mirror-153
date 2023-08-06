""" CLI Get options"""
import argparse
from typing import List, Optional

from mcli.cli.m_get import get_environment_variables, get_platforms, get_secrets, get_sweeps
from mcli.cli.m_get.display import OutputDisplay
from mcli.cli.m_get.runs import get_runs_argparser
from mcli.config import MCLIConfig


def get_entrypoint(parser, **kwargs) -> int:
    del kwargs
    parser.print_help()
    return 0


def add_common_arguments(parser: argparse.ArgumentParser):
    parser.add_argument('-o',
                        '--output',
                        type=OutputDisplay,
                        choices=list(OutputDisplay),
                        default=OutputDisplay.TABLE,
                        metavar='FORMAT',
                        help=f'Output display format. Should be one of {list(OutputDisplay)}')


def configure_argparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    subparsers = parser.add_subparsers(title='MCLI Objects',
                                       description='The table below shows the objects that you can get information on',
                                       help='DESCRIPTION',
                                       metavar='OBJECT')
    parser.set_defaults(func=get_entrypoint, parser=parser)

    conf = MCLIConfig.load_config(safe=True)
    if conf.internal:
        # TODO (HEK-473): Add back when projects are updated to new spec
        # projects_parser = subparsers.add_parser('projects', aliases=((((['project'])))), help='Get Project')
        # add_common_arguments(projects_parser)
        # projects_parser.set_defaults(func=get_projects)

        sweeps_parser = subparsers.add_parser('sweeps', aliases=['sweep'], help='Get Sweeps')
        add_common_arguments(sweeps_parser)
        sweeps_parser.set_defaults(func=get_sweeps)

    platform_parser = subparsers.add_parser('platforms', aliases=['platform'], help='List registered platforms')
    add_common_arguments(platform_parser)
    platform_parser.set_defaults(func=get_platforms)

    environment_parser = subparsers.add_parser('env',
                                               aliases=['environment', 'envs'],
                                               help='List registered environment variables')
    add_common_arguments(environment_parser)
    environment_parser.set_defaults(func=get_environment_variables)

    # pylint: disable-next=invalid-name
    SECRET_EXAMPLES = """

Examples:

> mcli get secrets
NAME         TYPE
foo          environment
docker-cred  docker_registry
file         mounted
    """
    secrets_parser = subparsers.add_parser(
        'secrets',
        aliases=['secret'],
        help='List registered secrets and credentials',
        description='List all of your registered secrets and credentials. Each '
        'listed secret will be added to your run automatically. For details on '
        'exactly how each type of secret is added to your run, look to the '
        'individual secret type docs.',
        epilog=SECRET_EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add_common_arguments(secrets_parser)
    secrets_parser.set_defaults(func=get_secrets)

    runs_parser = get_runs_argparser(subparsers)
    add_common_arguments(runs_parser)

    return parser


def add_get_argparser(subparser: argparse._SubParsersAction,
                      parents: Optional[List[argparse.ArgumentParser]] = None) -> argparse.ArgumentParser:
    """Adds the get parser to a subparser

    Args:
        subparser: the Subparser to add the Get parser to
    """
    del parents

    get_parser: argparse.ArgumentParser = subparser.add_parser(
        'get',
        aliases=['g'],
        help='Get info about objects created with mcli',
    )
    get_parser = configure_argparser(parser=get_parser)
    return get_parser
