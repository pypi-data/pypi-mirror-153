""" Automatic Deserialization for GraphQL Responses """
from dataclasses import asdict
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

import yaml

from mcli.api.schema.generic_model import DeserializableModel

# pylint: disable-next=invalid-name
T_DeserializableModel = TypeVar('T_DeserializableModel', bound=DeserializableModel)


class GenericResponse:
    """ Generic Response """
    success: bool
    message = None
    # pylint: disable-next=invalid-name
    messageLong = None
    item = None
    items = None

    def to_dict(self) -> Dict[str, Any]:
        """Converts the query into a dictionary
        """
        return {
            'success': self.success,
            'message': self.message,
            'messageLong': self.messageLong,
            'item': self.item,
            'items': self.items,
        }


class SuccessResponse(Generic[T_DeserializableModel], GenericResponse):
    """ Successful Response """
    success: bool
    message: Optional[str] = None
    # pylint: disable-next=invalid-name
    messageLong: Optional[str] = None
    item: Optional[T_DeserializableModel] = None
    items: Optional[List[T_DeserializableModel]] = None

    def __init__(
        self,
        success: bool,
        message: Optional[str] = None,
        # pylint: disable-next=invalid-name
        messageLong: Optional[str] = None,
        item: Optional[T_DeserializableModel] = None,
        items: Optional[List[T_DeserializableModel]] = None,
    ) -> None:
        """ A serialized Query Response

        Args:
            success: Whether the query has succeeded
            message: An Optional[str] message, usually used for errors
            messageLong: An Optional[str] longer message
            item: The Optional deserialized model object returned by GraphQL
            items: An Optional List of deserialized model objects returned by GraphQL
        """
        self.success = success
        self.message = message
        # pylint: disable-next=invalid-name
        self.messageLong = messageLong
        self.item = item
        self.items = items

    def __str__(self) -> str:
        return 'SuccessResponse:\n' + ('-' * 40) + '\n' + yaml.dump(self.to_dict())


class UnserializedSuccessResponse(Generic[T_DeserializableModel], GenericResponse):
    """ Unserialized Success Response """
    success: bool
    model_type: Optional[Type[T_DeserializableModel]]
    message: Optional[str] = None
    # pylint: disable-next=invalid-name
    messageLong: Optional[str] = None
    item: Optional[Dict[str, Any]] = None
    items: Optional[List[Dict[str, Any]]] = None

    def __init__(
        self,
        success: bool,
        model_type: Optional[Type[T_DeserializableModel]] = None,
        message: Optional[str] = None,
        # pylint: disable-next=invalid-name
        messageLong: Optional[str] = None,
        item: Optional[Dict[str, Any]] = None,
        items: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        """ An Unserialized Query Response that includes raw data

        Args:
            success: Whether the query has succeeded
            model_type: The Optional type of item or items in the return response. Must
                be of :type DeserializableModel:
            message: An Optional[str] message, usually used for errors
            messageLong: An Optional[str] longer message
            item: An Optional raw dictionary data that can be initialized into the
                `model_type`
            items: An Optional list of dictionary data which can be initialized into a
                List of DeserializedModel types
        """
        self.success = success
        self.model_type = model_type
        self.message = message
        # pylint: disable-next=invalid-name
        self.messageLong = messageLong
        self.item = item
        self.items = items

    def __str__(self) -> str:
        return 'UnserializedSuccessResponse:\n' + ('-' * 40) + '\n' + yaml.dump(asdict(self))

    def deserialize(self) -> SuccessResponse[T_DeserializableModel]:
        data = self.to_dict()
        if data['item']:
            assert self.model_type is not None, f"Please provide a model type to deserialize the item: {data['item']}"
            data['item'] = self.model_type(**self.model_type.translate_properties(properties=data['item']))
        if data['items']:
            assert self.model_type is not None, f"Please provide a model type to deserialize the items: {data['items']}"
            data['items'] = [
                # pylint: disable-next=not-an-iterable
                self.model_type(**self.model_type.translate_properties(properties=x)) for x in data['items']
            ]

        return SuccessResponse(**data)
