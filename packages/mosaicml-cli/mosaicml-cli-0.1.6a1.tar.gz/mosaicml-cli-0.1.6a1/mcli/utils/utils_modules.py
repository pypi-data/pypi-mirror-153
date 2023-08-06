""" Utils for python modules imports """
from importlib.util import find_spec


def check_if_module_exists(module_name: str) -> bool:
    """Checks if the module exists and is importable

    Args:
        module_name (str): The module to check

    Returns:
        True if the module is importable
    """
    return find_spec(name=module_name) is not None
