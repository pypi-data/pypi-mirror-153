"""Allows for Tree Generation of Configs"""
from typing import Any, Dict, List, Optional, Tuple

from rich.table import Table
from rich.tree import Tree

from mcli.utils.utils_wandb import get_diff


def dict_to_tree(data: Dict, tree: Optional[Tree] = None, style: Optional[str] = None, title: str = 'YAML') -> Tree:
    """Create a tree from a nested dictionary

    Use the ``rich.tree.Tree`` object to easily visualize nested dictioniaries in a tree form.
    This is great for printing configuration dictionaries to the console using ``rich.print``.

    Args:
        data (Dict): Nested dictionary
        tree (Tree, optional): Tree on which to add elements of the dictionary. Defaults to Tree(``title``).
        style (str, optional): One of ``rich``s styles. Defaults to ``None``.
        title (str, optional): The title for the Tree. Ignored if ``tree`` is passed. Defaults to ``"YAML"``.

    Returns:
        Tree: the nested tree corresponding to ``data``
    """
    if tree is None:
        tree = Tree(title)

    for k, v in data.items():
        inner = tree.add(k, style=style)
        if isinstance(v, dict):
            dict_to_tree(v, inner)  # Since style is inherited, we don't need to pass it to nested branches
        elif isinstance(v, str):
            inner.add(v)
        elif isinstance(v, (tuple, list)):
            for vv in v:
                inner.add(str(vv))
        else:
            inner.add(str(v))
    return tree


def _diff_dict_to_tree(diff: Dict, tree: Optional[Tree] = None) -> Tree:
    """See ``diff_dict_to_tree``.
    """
    if tree is None:
        tree = Tree('DIFF')
    for k, v in diff.items():
        inner = tree.add(k)
        if isinstance(v, dict):
            _diff_dict_to_tree(v, inner)
        elif isinstance(v, tuple):
            styles = ('bold', 'dim')
            for vv, style in zip(v, styles):
                if isinstance(vv, dict):
                    dict_to_tree(vv, inner.add('-', style=style), style=style)
                else:
                    inner.add(f'{vv}', style=style)
        else:
            raise TypeError('Leaf nodes should be tuples')
    return tree


def diff_dict_to_tree(c1: Dict, c2: Dict, tree: Optional[Tree] = None, title: str = 'DIFF') -> Tree:
    """Generate a tree of the differences between two dictionaries

    Use the ``rich.tree.Tree`` object to easily visualize the differences between two dictionaries in a tree form.
    This is great for printing these differences to the console using ``rich.print``.

    Args:
        c1, c2 (Dict): Two nested dictionaries to be compared
        tree (Tree, optional): Tree where the differences between ``c1`` and ``c2`` will be recorded.
                               Defaults to Tree(``title``).
        title (str, optional): The title for the Tree. Ignored if ``tree`` is passed. Defaults to ``"DIFF"``.

    Returns:
        Tree: The `rich.tree.Tree` object
    """
    if tree is None:
        tree = Tree(title)

    diff = get_diff(c1, c2)
    return _diff_dict_to_tree(diff, tree)


def create_table(data: List[Tuple[Any, ...]],
                 columns: List[str],
                 index_label: str = 'Index',
                 indices: Optional[List[Any]] = None,
                 table_kwargs: Optional[Dict[str, Any]] = None,
                 index_kwargs: Optional[Dict[str, Any]] = None,
                 column_kwargs: Optional[Dict[str, Any]] = None,
                 row_kwargs: Optional[Dict[str, Any]] = None) -> Table:
    """_summary_

    Args:
        data (List[Tuple[Any]]): _description_
        columns (Tuple[str]): _description_
        index_label (Optional[str]):
        indices (Optional[List[Any]], optional): _description_. Defaults to None.
        table_kwargs (Optional[Dict[str, Any]], optional): _description_. Defaults to None.
        index_kwargs (Optional[Dict[str, Any]], optional): _description_. Defaults to None.
        column_kwargs (Optional[Dict[str, Any]], optional): _description_. Defaults to None.
        row_kwargs (Optional[Dict[str, Any]], optional): _description_. Defaults to None.

    Returns:
        Table: _description_
    """

    if indices is None:
        indices = list(range(len(data)))
    if table_kwargs is None:
        table_kwargs = {}
    if column_kwargs is None:
        column_kwargs = {}
    if index_kwargs is None:
        index_kwargs = {}
    if row_kwargs is None:
        row_kwargs = {}

    data_table = Table(**table_kwargs)
    data_table.add_column(index_label, **index_kwargs)
    for column_name in columns:
        data_table.add_column(column_name, **column_kwargs)
    for idx, data_row in zip(indices, data):
        data_table.add_row(idx, *data_row, **row_kwargs)
    return data_table
