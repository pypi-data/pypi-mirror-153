""" Makes a dataclass Serializable to Disk and Back """
from dataclasses import dataclass, fields
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Generic, List, Optional, Tuple, Type, TypeVar, get_type_hints

from mcli.api.typing_future import get_args, get_origin

# pylint: disable-next=invalid-name
T_SerializableDataclass = TypeVar('T_SerializableDataclass', bound='SerializableDataclass')


@dataclass
class SerializableDataclass(Generic[T_SerializableDataclass]):
    """ A super class for Dataclasses that supports to_dict and from_dict

    Note: This super class does not support fancy typing, but does support
      - List[SerializableDataClass]
    """

    @classmethod
    def from_dict(
        cls: Type[T_SerializableDataclass],
        data: Dict[str, Any],
    ) -> T_SerializableDataclass:
        type_hints = get_type_hints(cls)

        for class_field in fields(cls):
            if class_field.name not in data:
                continue
            if class_field.name in type_hints:
                found_type: Type[Any] = type_hints[class_field.name]
                type_origin = get_origin(found_type)
                if type_origin in (list,):
                    type_args: Tuple[Type[Any]] = get_args(found_type)  # type: ignore
                    found_type = type_args[0]
                    if issubclass(found_type, SerializableDataclass):
                        data[class_field.name] = [found_type.from_dict(x) for x in data[class_field.name]]
                elif isinstance(found_type, Enum):
                    data[class_field.name] = found_type(data[class_field.name])
                elif found_type is datetime:
                    data[class_field.name] = datetime.fromisoformat(data[class_field.name])

        return cls(**data)

    @property
    def disk_skipped_fields(self) -> List[str]:
        """Fields to skip when serializing to be written to disk
        """
        return []

    def to_disk(self) -> Dict[str, Any]:
        """Get the current object as a dictionary to be written to disk

        Some objects need to skip fields when being written to persistent storage. Overriding the property
        ``disk_skipped_fields`` allows a subclass to do this.

        Raises:
            KeyError: Raised if a key to skip does not actually exist. This is likely to be an error.

        Returns:
            Dict[str, Any]: Dictionary representation of the object, with some fields skipped.
        """
        data = self.to_dict(to_disk=True)
        for field_key in self.disk_skipped_fields:
            if field_key not in data:
                raise KeyError(f'Key {field_key} does not exist')

        return {key: value for key, value in data.items() if key not in self.disk_skipped_fields}

    def to_dict(self, to_disk: bool = False) -> Dict[str, Any]:
        """Get the current object as a dictionary

        Args:
            to_disk: If true, call `to_disk` on any fields that are also ``SerializableDataclass` objects.
                Defaults to False.

        Returns:
            Dict[str, Any]: Dictionary representation of the object
        """

        def process_field_value(field_value: Any) -> Optional[Any]:
            """ Function that processes a field value based on its type into serializable form
            If a field value is an enum, it'll unpack it back to its serializable json value
            If a field is a list, it'll recursively process all elements
            """
            if isinstance(field_value, SerializableDataclass):
                if to_disk:
                    return field_value.to_disk()
                else:
                    return field_value.to_dict()
            elif isinstance(field_value, Enum):
                return field_value.value
            elif isinstance(field_value, datetime):
                return field_value.isoformat()
            elif isinstance(field_value, list):
                return [process_field_value(x) for x in field_value]
            elif field_value is not None:
                return field_value

        data = {}
        for class_field in fields(self):
            field_value = getattr(self, class_field.name)
            field_value = process_field_value(field_value)
            data[class_field.name] = field_value
        return data
