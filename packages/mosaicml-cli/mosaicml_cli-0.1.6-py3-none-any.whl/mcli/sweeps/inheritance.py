""" Inheritence from YAHP """
from __future__ import annotations

import collections.abc
import copy
import logging
import os
from typing import Any, Dict, List, Sequence, Tuple, TypeVar, Union, cast

import yaml

logger = logging.getLogger(__name__)


class ListOfSingleItemDict(list):
    """Simple list wrapper for a list of single-item dicts

    This enables string-based gets and sets. If there are duplicate keys in the list,
    the first one is retrieved/modified.
    """

    def __init__(self, data: List):
        super().__init__()
        if not is_list_of_single_item_dicts(data):
            raise TypeError('data must be list of single-item dictionaries')
        if isinstance(data, ListOfSingleItemDict):
            self._list = data._list
            self._data = data._data
        else:
            self._list = data
            self._data = cast(Dict, list_to_deduplicated_dict(data))

    def __contains__(self, key: Union[int, str]) -> bool:  # type: ignore
        return key in self._data

    def __getitem__(self, key: Union[int, str]) -> Any:  # type: ignore
        if key in self._data:
            return self._data[key]
        if not isinstance(key, int):
            raise TypeError(f'Index should be of type {int}, not {type(key)}')
        return self._list.__getitem__(key)

    def __setitem__(self, key, value):
        for item in self._list:
            k, _ = extract_only_item_from_dict(item)
            if k == key:
                item[k] = value
                self._data[key] = value
                return
        self._list.append({key: value})
        self._data[key] = value


# pylint: disable-next=invalid-name
JSON = Union[str, float, int, None, List['JSON'], Dict[str, 'JSON']]
# pylint: disable-next=invalid-name
JSON_NAMESPACE = Union[Dict[str, JSON], ListOfSingleItemDict, None]


def _get_inherits_paths(
    namespace: Dict[str, JSON],
    argument_path: List[str],
) -> List[Tuple[List[str], List[str]]]:
    """Finds all instances of 'inherits' in the dict `namespace`, along with their nested paths

    Args:
        namespace (Dict[str, JSON]): Nested dictionary in which to search
        argument_path (List[str]): List of keys in the nested dict relative to the original namespace

    Returns:
        List[Tuple[List[str], List[str]]]: List of paths and the files to be inherited from at each of those paths
    """
    paths: List[Tuple[List[str], List[str]]] = []
    for key, val in namespace.items():
        if key == 'inherits':
            if isinstance(val, str):
                val = [val]
            elif val is None:
                continue
            val = cast(List[str], val)
            paths.append((argument_path, val))
        elif isinstance(val, collections.abc.Mapping):
            paths += _get_inherits_paths(
                namespace=val,
                argument_path=argument_path + [key],
            )
    return paths


def _data_by_path(
    namespace: JSON,
    argument_path: Sequence[Union[int, str]],
) -> JSON:
    for key in argument_path:
        if isinstance(namespace, dict):
            assert isinstance(key, str)
            namespace = namespace[key]
        elif is_list_of_single_item_dicts(namespace):  #type: ignore
            assert isinstance(key, str)
            namespace = ListOfSingleItemDict(namespace)[key]  # type: ignore
        elif isinstance(namespace, list):
            assert isinstance(key, int)
            namespace = namespace[key]
        else:
            raise ValueError('Path must be empty unless if list or dict')
    return namespace


def _ensure_path_exists(namespace: JSON, argument_path: Sequence[Union[int, str]], is_list=False) -> None:
    for key in argument_path:
        if isinstance(namespace, dict):
            assert isinstance(key, str)
            default = [] if is_list else {}
            inner = namespace.setdefault(key, default)
        elif is_list_of_single_item_dicts(namespace):  #type: ignore
            assert isinstance(key, str)
            namespace = ListOfSingleItemDict(namespace)  #type: ignore
            if key not in namespace:
                namespace[key] = {}
            inner = namespace[key]

        elif isinstance(namespace, list):
            assert isinstance(key, int)
            inner = namespace[key]  # TODO: try except to verify key in range
        else:
            raise ValueError('Path must be empty unless if list or dict')
        if inner is None:
            namespace[key] = [] if is_list else {}  # type: ignore
            inner = namespace[key]  # type: ignore
        namespace = inner


class _OverriddenValue:

    def __init__(self, val: JSON):
        self.val = val


def _unwrap_overridden_value_dict(data: Dict[str, JSON]):
    for key, val in data.items():
        if isinstance(val, collections.abc.Mapping):
            _unwrap_overridden_value_dict(val)
        elif is_list_of_single_item_dicts(val):
            for item in val:  #type: ignore
                _unwrap_overridden_value_dict(item)
        elif isinstance(val, _OverriddenValue):
            data[key] = val.val


def _recursively_update_leaf_data_items(
    update_namespace: Dict[str, JSON],
    update_data: JSON,
    update_argument_path: List[str],
):
    if isinstance(update_data, collections.abc.Mapping):
        # This is still a branch point
        _ensure_path_exists(update_namespace, update_argument_path)
        for key, val in update_data.items():
            _recursively_update_leaf_data_items(
                update_namespace=update_namespace,
                update_data=val,
                update_argument_path=update_argument_path + [key],
            )

    elif is_list_of_single_item_dicts(update_data):
        assert isinstance(update_data, list)
        _ensure_path_exists(update_namespace, update_argument_path, is_list=True)
        for item in update_data:
            assert isinstance(item, dict)
            key, val = extract_only_item_from_dict(item)
            _recursively_update_leaf_data_items(
                update_namespace=update_namespace,
                update_data=val,
                update_argument_path=update_argument_path + [key],
            )
    else:
        # Must be a leaf
        inner_namespace = update_namespace

        # Traverse the tree to the final branch
        for key in update_argument_path[:-1]:
            key_element: JSON_NAMESPACE = None
            if isinstance(inner_namespace, collections.abc.Mapping):
                # Simple dict
                key_element = inner_namespace.get(key)  #type: ignore
            elif is_list_of_single_item_dicts(inner_namespace):
                # List of single-item dicts
                assert isinstance(inner_namespace, list)  # ensure type for pyright
                inner_namespace = ListOfSingleItemDict(inner_namespace)
                if key in inner_namespace:
                    key_element = inner_namespace[key]
            # key_element is None otherwise

            # This needs to be a branch, so make it an empty dict
            # This overrides simple types if the inheritance specifies a branch
            if key_element is None or not (isinstance(key_element, dict) or is_list_of_single_item_dicts(key_element)):
                key_element = {}
                inner_namespace[key] = key_element

            assert isinstance(key_element, dict) or is_list_of_single_item_dicts(key_element)
            inner_namespace = key_element

        key = update_argument_path[-1]
        if isinstance(inner_namespace, collections.abc.Mapping):
            existing_value = inner_namespace.get(key)
        else:
            # List of single-item dicts
            assert isinstance(inner_namespace, list)
            inner_namespace = ListOfSingleItemDict(inner_namespace)
            if key in inner_namespace:
                existing_value = inner_namespace[key]
            else:
                existing_value = None

        is_empty = (existing_value is None)  # Empty values should be filled in
        is_lower_priority = isinstance(existing_value, _OverriddenValue)  # Further inheritance should override previous
        is_inherits_dict = isinstance(existing_value,
                                      dict) and 'inherits' in existing_value  # Not sure about this one...

        if is_empty or is_lower_priority or is_inherits_dict:
            inner_namespace[key] = _OverriddenValue(update_data)  # type: ignore


def load_yaml_with_inheritance(yaml_path: str) -> Dict[str, JSON]:
    """Loads a YAML file with inheritance.

    Inheritance allows one YAML file to include data from another yaml file.

    Example:

    Given two yaml files -- ``foo.yaml`` and ``bar.yaml``:

    ``foo.yaml``:

    .. code-block:: yaml

        foo:
            inherits:
                - bar.yaml

    ``bar.yaml``:

    .. code-block:: yaml

        foo:
            param: val
            other:
                whatever: 12
        tomatoes: 11


    Then this function will return one dictionary with:

    .. code-block:: python

        {
            "foo": {
                "param": "val",
                "other: {
                    "whatever": 12
                }
            },
        }

    Args:
        yaml_path (str): The filepath to the yaml to load.

    Returns:
        JSON Dictionary: The flattened YAML, with inheritance stripped.
    """
    abs_path = os.path.abspath(yaml_path)
    file_directory = os.path.dirname(abs_path)
    with open(abs_path, 'r', encoding='utf8') as f:
        data: JSON = yaml.full_load(f)

    if data is None:
        data = {}

    assert isinstance(data, dict)

    # Get all instances of 'inherits' in the YAML, sorted by depth in the nested dict
    inherit_paths = sorted(_get_inherits_paths(data, []), key=lambda x: len(x[0]))

    for nested_keys, inherit_yamls in inherit_paths:
        for inherit_yaml in inherit_yamls:
            if not os.path.isabs(inherit_yaml):
                # Allow paths relative to the provided YAML
                inherit_yaml = os.path.abspath(os.path.join(file_directory, inherit_yaml))

            # Recursively load the YAML to inherit from
            inherit_data_full = load_yaml_with_inheritance(yaml_path=inherit_yaml)
            try:
                # Select out just the portion specified by nested_keys
                inherit_data = _data_by_path(namespace=inherit_data_full, argument_path=nested_keys)
            except KeyError as _:
                logger.warning(f'Failed to load item from inherited YAML file: {inherit_yaml}')
                continue

            # Insert any new keys from inherit_data into data
            _recursively_update_leaf_data_items(
                update_namespace=data,
                update_data=inherit_data,
                update_argument_path=nested_keys,
            )

        # Carefully remove the 'inherits' key from the nested data dict
        inherits_key_dict = _data_by_path(namespace=data, argument_path=nested_keys)
        if isinstance(inherits_key_dict, dict) and 'inherits' in inherits_key_dict:
            del inherits_key_dict['inherits']

    # Resolve all newly added values in data
    _unwrap_overridden_value_dict(data)
    return data


def preprocess_yaml_with_inheritance(yaml_path: str, output_yaml_path: str) -> None:
    """Helper function to preprocess yaml with inheritance and dump it to another file

    See :meth:`load_yaml_with_inheritance` for how inheritance works.

    Args:
        yaml_path (str): Filepath to load
        output_yaml_path (str): Filepath to write flattened yaml to.
    """
    data = load_yaml_with_inheritance(yaml_path)
    with open(output_yaml_path, 'w+', encoding='utf8') as f:
        yaml.dump(data, f, explicit_end=False, explicit_start=False, indent=2, default_flow_style=False)  # type: ignore


# pylint: disable-next=invalid-name
T_K = TypeVar('T_K')
# pylint: disable-next=invalid-name
T_V = TypeVar('T_V')


def extract_only_item_from_dict(val: Dict[T_K, T_V]) -> Tuple[T_K, T_V]:
    """Extracts the only item from a dict and returns it .

    Args:
        val (Dict[T_K, T_V]): A dictionary which should contain only one entry

    Raises:
        ValueError: Raised if the dictionary does not contain 1 item

    Returns:
        Tuple[T_K, T_V]: The key, value pair of the only item
    """
    if len(val) != 1:
        raise ValueError(f'dict has {len(val)} keys, expecting 1')
    return list(val.items())[0]


def list_to_deduplicated_dict(
    list_of_dict: List[JSON],
    allow_str: bool = False,
    separator: str = '+',
) -> Dict[str, JSON]:
    """Converts a list of single-item dictionaries to a dictionary, deduplicating keys along the way

    Args:
        list_of_dict (List[Dict[str, Any]]): A list of single-item dictionaries
        allow_str (bool, optional): If True, list can contain strings, which will be added as keys with None values.
                                    Defaults to False.
        separator (str, optional): The separator to use for deduplication. Default '+'.

    Returns:
        Dict[str, Dict]: Deduplicated dictionary
    """

    data: JSON = {}
    counter: Dict[str, int] = {}
    for item in list_of_dict:
        if isinstance(item, str) and allow_str:
            k, v = item, None
        elif isinstance(item, dict):
            # item should have only one key-value pair
            k, v = extract_only_item_from_dict(item)
        else:
            raise TypeError(f'Expected list of dictionaries, got {type(item)}')
        if k in data:
            # Deduplicate by add '+<counter>'
            counter[k] += 1
            k = ''.join((k, separator, str(counter[k] - 1)))
        else:
            counter[k] = 1
        data[k] = v
    return data


def is_list_of_single_item_dicts(obj: JSON) -> bool:
    """Whether the provided object is a list of single-item dictionaries

    Args:
        obj (List[Dict]) - Possible list of dictionaries

    Returns:
        True if ``obj`` is a list of single-item dictionaries
    """

    if isinstance(obj, ListOfSingleItemDict):
        return True

    if not isinstance(obj, list):
        return False

    for item in obj:
        if not (isinstance(item, dict) and len(item) == 1):
            return False

    return True


def merge(base: Dict[str, JSON], head: Dict[str, JSON]) -> Dict[str, JSON]:
    """Merge two dictionaries using YAHP-based inheritance tools.

    Args:
        base (Dict[str, JSON]): Base JSON dictionary. Values will be appended but not overwritten
        head (Dict[str, JSON]): Head JSON dictionary from which to inherit new values

    Returns:
        Dict[str, JSON]: Merge JSON dictionary

    Note:
    This method will be deprecated when we create a proper JSON-merge solution
    """
    base = copy.deepcopy(base)
    _recursively_update_leaf_data_items(base, head, [])
    _unwrap_overridden_value_dict(base)
    return base
