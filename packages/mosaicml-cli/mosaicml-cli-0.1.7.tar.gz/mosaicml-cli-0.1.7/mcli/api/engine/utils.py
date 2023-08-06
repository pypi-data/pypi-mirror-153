""" Engine Utils """
from textwrap import dedent, indent


def dedent_indent(text: str, indentation: int = 0) -> str:
    """Unindents a block of text, then reindents it

    Args:
        text: The text to indent
        indentation: The amount to reindent the text

    Returns:
        The dedented then indented text
    """

    return indent(dedent(text.strip()), indentation * ' ')
