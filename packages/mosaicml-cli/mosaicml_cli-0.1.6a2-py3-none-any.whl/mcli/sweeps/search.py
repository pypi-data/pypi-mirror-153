""" Grid Search """
import itertools
from typing import Any, Dict, List

from mcli.utils.utils_types import dot_to_nested


def grid_search(parameters: Dict[str, List[Any]]) -> List[Dict[str, Any]]:
    """Generate a grid search over the provided parameters

    Args:
        parameters (Dict[str, List[Any]]): A dot-syntax dictionary of parameters to form a grid over.
                                           Each item should be a dot-syntax key (e.g. 'a.b.c') with a list of values
                                           (e.g. ['foo', 'bar', 'baz']).

    Returns:
        List[Dict[str, Any]]: A list of nested dictionaries, one for each node on the parameter grid.
    """
    # performs the product:
    # {'a': [1,2,3], 'b': [True, False]} --> [{'a': 1, 'b': True}, {'a': 1', 'b': False}, ...]

    sweep = []
    if len(parameters) > 0:
        keys, values = zip(*parameters.items())
        for val in itertools.product(*values):
            params = dict(zip(keys, val))
            sweep.append(dot_to_nested(params))  # type: ignore
    else:
        sweep.append({})

    return sweep
