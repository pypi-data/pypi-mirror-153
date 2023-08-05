# -*- coding: utf-8 -*-
import base64
import datetime
import json
from json import JSONDecodeError
from typing import Optional, Any

from pip_services3_commons.convert import StringConverter, DateTimeConverter
from pip_services3_commons.data import IdGenerator


class MessageEnvelope:
    """
    Allows adding additional information to messages. A correlation id, message id, and a message type
    are added to the data being sent/received. Additionally, a MessageEnvelope can reference a lock token.

    Side note: a MessageEnvelope's message is stored as a buffer, so strings are converted
    using utf8 conversions.
    """

    def __init__(self, correlation_id: Optional[str], message_type: Optional[str], message: Optional[Any]):
        """
        Creates a new MessageEnvelope, which adds a correlation id, message id, and a type to the
        data being sent/received.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param message_type: a string value that defines the message's type.
        :param message: the data being sent/received.
        """
        self.__reference: Any = None
        # The unique business transaction id that is used to trace calls across components.
        self.correlation_id = correlation_id
        # String value that defines the stored message's type.
        self.message_type = message_type
        # The message's auto-generated ID.
        self.message_id: str = None
        # The time at which the message was sent.
        self.sent_time: datetime.datetime = None
        # The stored message.
        self.message: bytes = None

        if isinstance(message, bytes):
            self.message = message
        if isinstance(message, str):
            self.set_message_as_string(message)
        else:
            self.set_message_as_object(message)

        self.message_id = IdGenerator.next_long()

    def get_reference(self) -> Any:
        """
        Gets a lock token reference for this MessageEnvelope.

        :return: the lock token that this MessageEnvelope references.
        """
        return self.__reference

    def set_reference(self, value: Any):
        """
        Sets a lock token reference for this MessageEnvelope.

        :param value: the lock token to reference.
        """
        self.__reference = value

    def get_message_as_string(self) -> Optional[str]:
        """
        Returns string the information stored in this message as a UTF-8 encoded string.

        :return: the information stored in this message as a UTF-8 encoded string.
        """
        return self.message.decode('utf-8') if self.message is not None else None

    def set_message_as_string(self, value: str):
        """
        Stores the given string.

        :param value: the string to set. Will be converted to a buffer, using UTF-8 encoding.
        """
        self.message = value.encode('utf-8')

    def get_message_as(self) -> Any:
        """
        Returns any the value that was stored in this message as a JSON string.

        :return: the value that was stored in this message as a JSON string.
        """
        if self.message is None: return
        temp = self.message.decode('utf-8')
        return json.loads(temp)

    def set_message_as_object(self, value: Any):
        """
        Stores the given value as a object.

        :param value: the value to convert to JSON and store in  this message.
        """
        if value is None:
            self.message = None
        else:
            temp = json.dumps(value)
            self.message = temp.encode('utf-8')

    def to_string(self) -> str:
        """
        Convert's this MessageEnvelope to a string, using the following format:
        ```"[<correlation_id>,<message_type>,<message.toString>]"```.

        If any of the values are ```None```, they will be replaced with ```---```.

        :return: the generated string.
        """
        builder = '['
        builder += self.correlation_id or ''
        builder += self.correlation_id or "---"
        builder += ','
        builder += self.message_type or "---"
        builder += ','
        builder += "---" if not self.message else self.message[0:50].decode('utf8')
        builder += ']'
        return builder

    def __str__(self):
        return self.to_string()

    def to_json(self) -> dict:
        """
        Converts this MessageEnvelope to a JSON string.
        The message payload is passed as base64 string

        :return: A JSON encoded representation is this object.
        """
        payload = None if not self.message else base64.b64encode(self.message)
        jsoon = {
            'message_id': self.message_id,
            'correlation_id': self.correlation_id,
            'message_type': self.message_type,
            'sent_time': StringConverter.to_string(
                datetime.datetime.now().isoformat() if not self.sent_time else self.sent_time.isoformat()),
            'message': payload.decode('utf-8')
        }
        return jsoon

    @staticmethod
    def from_json(value: str) -> Optional['MessageEnvelope']:
        """
        Converts a JSON string into a MessageEnvelope
        The message payload is passed as base64 string

        :param value: a JSON encoded string
        :return: a decoded Message Envelop.
        """
        if value is None: return

        jsoon: Any
        try:
            jsoon = json.loads(value)
        except JSONDecodeError:
            return

        message = MessageEnvelope(jsoon['correlation_id'], jsoon['message_type'], None)
        message.message_id = jsoon['message_id']
        message.message = None if not jsoon['message'] else base64.b64decode(jsoon['message'])
        message.sent_time = DateTimeConverter.to_nullable_datetime(jsoon['sent_time'])

        return message
