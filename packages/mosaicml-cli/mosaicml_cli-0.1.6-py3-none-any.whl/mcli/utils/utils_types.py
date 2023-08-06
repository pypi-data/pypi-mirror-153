"""Type Utils for converting between nested structures"""
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Type, TypeVar, Union

from mcli.sweeps.inheritance import ListOfSingleItemDict, extract_only_item_from_dict, is_list_of_single_item_dicts

PathLike = Union[str, Path]
EnumType = TypeVar('EnumType', bound=Enum)  # pylint: disable=invalid-name


class CommonEnum(Enum):
    """Base class for enums that provides a proper __str__ method and ensure_enum
    """

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def ensure_enum(cls: Type[EnumType], val: Union[str, EnumType]) -> EnumType:
        if isinstance(val, str):
            try:
                return cls[val]
            except KeyError as e:
                valid = ', '.join(str(x) for x in cls)
                raise ValueError(f'Invalid {cls.__name__}: got {val}. Must be one of: {valid}') from e

        elif isinstance(val, cls):
            return val
        raise ValueError(f'Unable to ensure {val} is a {cls.__name__} enum')


def get_hours_type(max_value: float) -> Callable[[Union[str, float]], float]:
    """Returns a type checker that verifies a value is a float and lies between 0 and max_value
    """

    def _validate_hours(value: Union[str, float]) -> float:
        float_value: float = float(value)
        if float_value <= 0 or float_value > max_value:
            raise ValueError(
                f'The value for `--hours` must be a float between 0 and {max_value}, but {float_value} was specified. '
                'Please specify a value within this range.')
        return float_value

    return _validate_hours


def dot_to_nested(config: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a dot-syntax dictionary to a nested dictionary

    Takes as input a dot-syntax dictionary, e.g.
    ```
    config = {"a.b.c": "foo",
              "a.b.d": "bar"}
    ```
    and outputs a nested dictionary, e.g.
    ```
    dot_to_nested(config) == {"a": {"b": {"c": "foo", "d": "bar"}}}
    ```

    Arguments:
        config (Dict[str, Any]): A dot-syntax dictionary

    Returns:
        Dict[str, Any]: A nested dictionary
    """

    nested = {}
    for dot_key, v in config.items():
        keys = dot_key.split('.')
        inner = nested
        for key in keys[:-1]:
            inner = inner.setdefault(key, {})
        inner[keys[-1]] = v
    return nested


def nested_to_dot(data: Dict[str, Any], separator: str = '.') -> Dict[str, Any]:
    """
    Flattens a dictionary with list or sub dicts to have dot syntax
    i.e. {
        "sub_dict":{
        "sub_list":[
            "sub_sub_dict":{
            "field1": 12,
            "field2": "tomatoes"
            }
        ]
        },
        "field3": "potatoes"
    }
    returns:
    {
        "sub_dict.sub_list.sub_sub_dict.field1": 12,
        "sub_dict.sub_list.sub_sub_dict.field2": "tomatoes,
        "field3": "potatoes",
    }
    """

    def get_flattened_dict(d, _prefix, separator):
        all_items = {}
        for key, val in d.items():
            key_items = _prefix + [key]
            key_name = separator.join(key_items)
            if isinstance(val, dict):
                all_items.update(get_flattened_dict(val, key_items, separator))
            elif isinstance(val, list):
                found_sub_dicts = False
                for item in val:
                    if isinstance(item, dict):
                        found_sub_dicts = True
                        for sub_key, sub_val in item.items():
                            all_items.update(get_flattened_dict(sub_val, key_items + [sub_key], separator))
                if not found_sub_dicts:
                    all_items[key_name] = val
            else:
                all_items[key_name] = val
        return all_items

    return get_flattened_dict(data, [], separator)


def convert_dict_to_single_item_lists(config: Dict[str, Any], keys: List[str]) -> Dict[str, Any]:
    """Converts specific keys in a nested dict to single-item lists

    Specific versions of YAHP require that certain keys are lists of single-item dictionaries. This is fixed in the
    most recent version, but that change has not propogated reliably to users yet. In the meantime, we need to ensure
    that composer gets configurations in the format it expects.

    Args:
        config (Dict[str, Any]): Nested configuration dictionary
        keys (List[str]): List of keys to convert to single-item lists

    Returns:
        Dict[str, Any]: Modified configuration dictionary
    """
    for k in keys:
        if k in config:
            if isinstance(config[k], dict):
                config[k] = [{kk: v} for kk, v in config[k].items()]
    return config


def _list_to_dict(item):
    if is_list_of_single_item_dicts(item):
        new_item = {}
        for kv in item:
            k, v = extract_only_item_from_dict(kv)
            new_item[k] = v
    else:
        new_item = item

    return new_item


def convert_single_item_lists_to_dict(config: Dict[str, Any]) -> Dict[str, Any]:
    """Converts any single-item lists in a nested dict to dicts

    Args:
        config (Dict[str, Any]): Nested configuration dictionary

    Returns:
        Dict[str, Any]: Entirely nested configuration dictionary
    """

    if is_list_of_single_item_dicts(config):
        config = _list_to_dict(config)
    if not isinstance(config, dict):
        raise TypeError(f'config must be a dict or list of single-item dicts. Got {type(config)}')

    for k, v in config.items():
        if isinstance(v, dict):
            convert_single_item_lists_to_dict(v)
        elif is_list_of_single_item_dicts(v):
            config[k] = _list_to_dict(v)
            convert_single_item_lists_to_dict(config[k])

    return config


def delete_nested_key(config: Dict[str, Any], keys: List[str]) -> Dict:
    """Delete the specied key nested within ``config``.

    Args:
        config (Dict): Nested dictionary
        keys (str): A list of keys within the nested dict

    Returns:
        Dict: ``config`` with the key deleted. Deletion is done in-place,
             so the output is provided as a convenience only.

    Examples:
        config = {'a': {'b': 'foo', 'c': 'bar'}}
        config = delete_nested_key(config, ['a', 'b'])
        config == {'a': {'c': 'bar'}}
    """
    if isinstance(keys, str):
        keys = list(keys.split('.'))
    inner = config

    # Recurse to last key within the nested dict
    for key in keys[:-1]:
        if is_list_of_single_item_dicts(inner):
            assert isinstance(inner, list)
            inner = ListOfSingleItemDict(inner)
        if key not in inner:  # higher key isn't there, so no need to go further
            return config
        inner = inner[key]

    # Remove last key, if it exists
    key = keys[-1]
    if is_list_of_single_item_dicts(inner):  # Handle special lists
        assert isinstance(inner, list)
        item_index: int = -1
        for ii, item in enumerate(inner):
            if key in item:
                item_index = ii
        if item_index > -1:
            inner.pop(item_index)
    elif isinstance(inner, dict):
        inner.pop(keys[-1], None)
    return config
