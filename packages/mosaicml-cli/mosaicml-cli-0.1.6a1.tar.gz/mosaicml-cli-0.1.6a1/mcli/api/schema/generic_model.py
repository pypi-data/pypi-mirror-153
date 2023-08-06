""" Generic GraphQL Helpers """
from abc import ABC
from datetime import datetime
from typing import Any, Dict, List, Tuple, Type, Union, cast, get_type_hints

from mcli.api.typing_future import get_args, get_origin  # type: ignore - unknown import symbol


class DeserializableModel(ABC):
    """ A model type that is deserializable with extra defined helpers

    Helps automatically convert to snake_case for variable names
    Helps automatically convert values into their correct types
    """

    property_translations: Dict[str, str]
    datetime_fields: List[str]

    # pylint: disable-next=useless-super-delegation
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    @classmethod
    def _translate_value_for_field(
        cls: Type[Any],
        field: str,
        value: Any,
    ) -> Any:
        """Translates a single field value pair with deserialization into the
        correct dataclass typed fields

        Args:
            field: The string name of the property/field
            value: The raw value of the field to deserialize

        Returns:
            Returns the deserialized value of the field for the given dataclass
            object
        """
        type_hints = get_type_hints(cls)
        if field in type_hints:
            found_type: Type[Any] = type_hints[field]
            # TODO: Check None in get_args works properly
            if get_origin(found_type) == Union and type(None) in get_args(found_type):  # type: ignore
                # Unwrap optional type
                type_args: Tuple[Type[Any]] = get_args(found_type)  # type: ignore
                found_type = type_args[0]

            found_type_origin = get_origin(found_type)
            if found_type is DeserializableModel:
                assert isinstance(found_type, DeserializableModel)
                new_properties = found_type.translate_properties(properties=value)
                return found_type(**new_properties)
            elif found_type is datetime:
                if isinstance(value, str):
                    # Convert from the postgres string to something python-compatible
                    value = value.replace('Z', '+00:00')
                    value = datetime.fromisoformat(value)
                return value
            elif found_type_origin == list:
                type_list = get_args(found_type)
                type_list = cast(List[Type[Any]], type_list)
                assert len(type_list) > 0
                iterable_type: Type[Any] = type_list[0]
                if isinstance(iterable_type, DeserializableModel):
                    return [iterable_type(**iterable_type.translate_properties(properties=v)) for v in value]

                # TODO: I'm pretty sure a bug was introduced in this case
                #       future self, pls look into in future
                return found_type_origin(value)  # type: ignore

            elif found_type_origin == dict:
                assert isinstance(value, dict)
                type_list = get_args(found_type)
                type_list = cast(List[Type[Any]], type_list)
                assert len(type_list) > 1
                value_type: Type[Any] = type_list[1]
                for k, v in value.items():
                    if isinstance(value_type, DeserializableModel):
                        v = value_type(**value_type.translate_properties(properties=v))
                    value[k] = v
                return value
            else:
                return found_type(value)

        return value

    @classmethod
    def translate_properties(cls, properties: Dict[str, Any]) -> Dict[str, Any]:
        """Translates properties of type Dict[str,Any] to the corresponding
        dataclass field types

        Deserialized a GraphQL dictionary that is meant to be a :type
        DeserializableModel: dataclass, ensuring that all fields are casted to
        the correct type for the dataclass. `translate_properties` will
        recursively deserialize GraphQL objects, even if they are nested.
        `translate_properties` also deals with field renaming with the different
        naming conventions, such as camelCase to snake_case in the transition
        from typescript to python.

        Args:
            properties: The raw Dict[str,Any] returned by GraphQL for
                deserialization

        Returns:
            Returns a dictionary of keys and values that can be used to
            directly initialize the DeserializableModel from kwargs
        """
        data = {}
        for k, v in properties.items():
            if k in cls.property_translations:
                if cls.property_translations[k] is not None:
                    k = cls.property_translations[k]
            v = cls._translate_value_for_field(
                field=k,
                value=v,
            )
            data[k] = v
        return data
