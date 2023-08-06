"""Utils for logging"""
import logging
import textwrap

from rich import print as rprint
from rich.console import Console
from rich.highlighter import NullHighlighter
from rich.logging import RichHandler
from rich.theme import Theme
from rich.tree import Tree

console = Console()
err_console = Console(stderr=True)

FAIL = '[red]✗[/] '
OK = '[green]✔[/] '
INFO = '[blue]i[/] '
QUESTION = '? '  # Placeholder for a colored question mark
WARN = '[red bold]![/] '


class TreeCompatibleHandler(RichHandler):
    """Logs messages using the ``RichHandler``, with support for ``rich.tree.Tree`` objects.

    NOTE: Currently only supports printing the Tree on stdout.
    TODO (TL): Add support for printing to stderr
    """

    def emit(self, record) -> None:
        if record.levelno >= self.level and isinstance(record.msg, Tree):
            rprint(record.msg)
        else:
            super().emit(record)


console_handler = TreeCompatibleHandler(show_time=False,
                                        show_level=False,
                                        show_path=False,
                                        console=Console(stderr=True, theme=Theme({'file': 'bold blue'})),
                                        highlighter=NullHighlighter())

console_handler.setFormatter(logging.Formatter(fmt='%(message)s'))
console_handler.markup = True


def log_tree(tree: Tree, level: str, logger: logging.Logger) -> None:

    mapping = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARN': logging.WARN,
        'ERROR': logging.ERROR,
    }
    try:
        level_val: int = mapping[level.upper()]
        if level_val >= logger.level:
            logger.log(level_val, '')
            rprint(tree)
            logger.log(level_val, '')
    except KeyError as key_error:
        raise ValueError(f'Invalid log level {level}. Should be one of {list(mapping.keys())}') from key_error


def get_indented_block(text: str, indent: int = 4, marker: str = ' ', remove_indent: bool = True) -> str:
    """Get an indented block of text from a multi-line string

    Args:
        text: A possibly multi-line string of text
        indent: Number of indents for the block. Defaults to 4.
        marker: String to use as the indent. Defaults to ' '.
        remove_indent: Remove existing indent. Defaults to True.

    Returns:
        An indented block of text
    """

    def strip(ss: str):
        if remove_indent:
            return ss.strip()
        else:
            return ss.rstrip()

    text = ' '.join([strip(line) for line in text.splitlines() if strip(line) != ''])
    wrapped = textwrap.wrap(text, console.width - 2 * indent)
    block = textwrap.indent('\n'.join(wrapped), prefix=marker * indent)
    return block
