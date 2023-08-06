""" Adds MUtil as a lazy loaded package """
import argparse


def add_util_argparser(subparser: argparse._SubParsersAction,):
    """Adds the util parser to a subparser if mutil is installed

    Args:
        subparser: the Subparser to add the Get parser to
    """

    # Automatically uses mutil as external package if installed
    try:
        # pylint: disable-next=import-outside-toplevel
        from mutil.cli import configure_parser  # type: ignore
        # pylint: disable-next=import-outside-toplevel
        from mutil.util import get_util  # type: ignore
    except:  # pylint: disable=bare-except
        return

    util_parser: argparse.ArgumentParser = subparser.add_parser(
        'util',
        help='Get cluster utilization.  Note: You must have mosaicml-mutil pip installed',
    )

    configure_parser(util_parser)
    util_parser.set_defaults(func=get_util)

    return util_parser
