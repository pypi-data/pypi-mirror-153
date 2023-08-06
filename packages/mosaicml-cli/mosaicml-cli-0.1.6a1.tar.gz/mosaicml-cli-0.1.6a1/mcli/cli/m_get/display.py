"""Helpers for `mcli get` displays"""
import datetime
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from enum import Enum
from typing import Any, Dict, Generator, List, Optional, Tuple

from rich.table import Table

from mcli.utils.utils_logging import console, err_console
from mcli.utils.utils_rich import create_table


class OutputDisplay(Enum):
    TABLE = 'table'
    NAME = 'name'
    JSON = 'json'

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self.value)


@dataclass
class MCLIDisplayItem():
    """Item for display in an `mcli get` list of items
    """
    name: str

    def to_dict(self) -> Dict[str, Any]:
        """Get the current object as a dictionary

        Returns:
            Dict[str, Any]: Dictionary representation of the object
        """

        def process_field_value(field_value: Any) -> Optional[Any]:
            """ Function that processes a field value based on its type into serializable form
            If a field value is an enum, it'll unpack it back to its serializable json value
            If a field is a list, it'll recursively process all elements
            """

            if isinstance(field_value, Enum):
                return str(field_value.value)
            elif isinstance(field_value, datetime.datetime):
                return field_value.isoformat()
            elif field_value is not None:
                return str(field_value)

        data = {}
        for class_field in fields(self):
            field_value = getattr(self, class_field.name)
            field_value = process_field_value(field_value)
            data[class_field.name] = field_value
        return data


class MCLIGetDisplay(ABC):
    """ABC for all `mcli get` lists
    """

    def print(self, output: OutputDisplay):
        items = self.get_list()
        if not items:
            err_console.print('None')
            return
        if output == OutputDisplay.TABLE:
            disp = self.to_table(items)
        elif output == OutputDisplay.NAME:
            names = self.to_name(items)
            disp = '\n'.join(names)
        elif output == OutputDisplay.JSON:
            json_list = self.to_json(items)
            disp = json.dumps(json_list)
        else:
            raise ValueError(f'output is not a known display type. It must be one of {list(OutputDisplay)}')
        console.print(disp)

    def get_list(self) -> List[Dict[str, Any]]:
        return [item.to_dict() for item in self]

    def to_table(self, items: List[Dict[str, Any]]) -> Table:
        column_names = [key for key in items[0] if key != 'name']
        columns, names = [], []
        for item in items:
            names.append(item['name'])
            columns.append(tuple(item[key] for key in column_names))
        return create_display_table(names, columns, column_names)

    def to_name(self, items: List[Dict[str, Any]]) -> List[str]:
        return [item['name'] for item in items]

    def to_json(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return items

    @abstractmethod
    def __iter__(self) -> Generator[MCLIDisplayItem, None, None]:
        ...


def create_display_table(names: List[str], columns: List[Tuple[Any, ...]], column_names: List[str]) -> Table:

    output_table = create_table(data=columns,
                                indices=names,
                                index_label='NAME',
                                columns=[ss.upper() for ss in column_names],
                                table_kwargs={
                                    'box': None,
                                    'pad_edge': False
                                },
                                index_kwargs={
                                    'justify': 'left',
                                    'no_wrap': True
                                })
    return output_table
