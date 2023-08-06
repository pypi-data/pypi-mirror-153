""" m view Entrypoint """
import argparse


def view(args) -> int:
    print('Running')
    print(args)

    return 0


def add_view_argparser(parent_parser: argparse._SubParsersAction) -> None:
    parser = parent_parser.add_parser('view', aliases=['v'], help='View stuff')
    parser.set_defaults(func=view)
