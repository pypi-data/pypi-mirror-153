"""Utility functions for the CLI and CLI testing"""
import sys
from contextlib import contextmanager
from typing import List


@contextmanager
def set_argv(args: List[str]):
    """Temporarily override sys.argv

    Args:
        args (List[str]): List of new args
    """
    original_argv = sys.argv
    sys.argv = args
    yield
    sys.argv = original_argv
