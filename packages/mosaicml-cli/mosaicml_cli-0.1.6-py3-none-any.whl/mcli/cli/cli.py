#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

""" MCLI Entrypoint """

import argparse
import itertools
import logging
import sys
from string import ascii_lowercase

import argcomplete

from mcli.cli.m_clean.m_clean import clean_mcli
from mcli.cli.m_create.m_create import add_create_argparser
from mcli.cli.m_delete.m_delete import add_delete_argparser
from mcli.cli.m_get.m_get import add_get_argparser
from mcli.cli.m_init.m_init import initialize_mcli
from mcli.cli.m_init.m_init_kube import add_init_kube_parser
from mcli.cli.m_interactive.m_interactive import add_interactive_argparser
from mcli.cli.m_log.m_log import add_log_parser
from mcli.cli.m_root.m_config import m_get_config
from mcli.cli.m_root.m_util import add_util_argparser
from mcli.cli.m_run.m_run import add_run_argparser
from mcli.cli.m_use.m_use import add_use_argparser
from mcli.config import MCLIConfig
from mcli.utils.utils_logging import console_handler
from mcli.utils.utils_pypi import NeedsUpdateError, check_new_update_available
from mcli.version import print_version

logger = logging.getLogger('mcli')
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)


def test_mcli(**kwargs) -> int:
    """Testing stub function

    Args:
        **kwargs:
    """
    conf = MCLIConfig.load_config(safe=True)
    print(conf)
    del kwargs
    return 0


def add_root_commands(subparser: argparse._SubParsersAction,) -> None:
    """Adds root level commands to the CLI

    Args:
        subparser: The subparser to add commands to
    """

    conf = MCLIConfig.load_config(safe=True)
    config_parser: argparse.ArgumentParser = subparser.add_parser(
        'config', aliases=['c'], help='Printout the config of the current MCLI project')
    config_parser.set_defaults(func=m_get_config)

    # TODO(HEK-414): Refactor sweep to be up to date
    def _sweep_entry(**kwargs) -> int:
        del kwargs
        print('MCLI Sweep is currently unsupported.  Please use mcli run instead')
        return 1

    sweep_parser: argparse.ArgumentParser = subparser.add_parser('sweep', help='MCLI Sweep is currently Unsupported')
    sweep_parser.set_defaults(func=_sweep_entry)

    init_parser: argparse.ArgumentParser = subparser.add_parser('init', aliases=['i'], help='Initialize MCLI')
    init_parser.set_defaults(func=initialize_mcli)

    version_parser: argparse.ArgumentParser = subparser.add_parser('version', help='MCLI Version')
    version_parser.set_defaults(func=print_version)

    if conf.internal:
        clean_parser: argparse.ArgumentParser = subparser.add_parser('clean', aliases=['cl'], help='Clean MCLI')
        clean_parser.set_defaults(func=clean_mcli)
        if conf.dev_mode:
            clean_parser.add_argument('--remove_db',
                                      action='store_true',
                                      default=False,
                                      help='Delete the FeatureDB Also')

    if conf.dev_mode:
        test_parser: argparse.ArgumentParser = subparser.add_parser('test', aliases=['t'], help='Test stub')
        test_parser.set_defaults(func=test_mcli)


def get_parser() -> argparse.ArgumentParser:
    """The main parser
    """

    # Add common `mcli` arguments to a parent parser. These should be used by all subparsers.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument('-v', '--verbose', action='count', help='Increase CLI verbosity', default=0)
    parents = [common]

    parser = argparse.ArgumentParser(prog='mcli', parents=parents)
    subparser = parser.add_subparsers(title='MCLI Commands',
                                      description='The table below shows the commands that are available',
                                      help='DESCRIPTION',
                                      metavar='COMMAND')

    def print_help(**kwargs):
        del kwargs
        parser.print_help()

    parser.set_defaults(func=print_help)

    add_root_commands(subparser=subparser)
    add_init_kube_parser(subparser=subparser)
    add_run_argparser(subparser=subparser)
    add_create_argparser(subparser=subparser)
    add_get_argparser(subparser=subparser, parents=parents)
    add_delete_argparser(subparser=subparser)
    add_log_parser(subparser=subparser)

    conf = MCLIConfig.load_config(safe=True)
    if conf.internal:
        add_interactive_argparser(subparser=subparser)
        add_util_argparser(subparser=subparser)
        add_use_argparser(subparser=subparser)
        # TODO(HEK-414): Refactor sweep to be up to date
        # add_sweep_argparser(subparser=subparser)

    return parser


def main() -> int:
    """The main entrypoint
    """

    parser = get_parser()
    aliases = list(ascii_lowercase) + [''.join(i) for i in itertools.product(ascii_lowercase, repeat=2)]
    argcomplete.autocomplete(
        parser,
        exclude=aliases,
        always_complete_options='long',  # type: ignore
    )

    try:
        check_new_update_available()
    except NeedsUpdateError:
        return 1

    args = parser.parse_args()

    if len(vars(args)) == 0:
        parser.print_help()
        return 0

    if args.verbose >= 1:
        logger.setLevel(logging.DEBUG)

    console_handler.markup = True

    var_args = vars(args)
    del var_args['verbose']
    try:
        return args.func(**var_args)
    except KeyboardInterrupt as k:
        del k
        logger.info('\nExiting with Keyboard Interrupt')
        return 1
    except Exception as e:
        raise e


if __name__ == '__main__':
    sys.exit(main())
