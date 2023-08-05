# -*- coding: utf-8 -*-
import threading
from typing import List, Optional

from pip_services3_commons.run import ICleanable

from pip_services3_messaging.queues import IMessageReceiver, MessageEnvelope, IMessageQueue


class TestMessageReceiver(IMessageReceiver, ICleanable):
    """
    TODO add description
    """

    def __init__(self):
        self.__messages: List[MessageEnvelope] = []
        self.__lock = threading.Lock()

    @property
    def messages(self) -> List[MessageEnvelope]:
        """
         Gets the list of received messages.
        """
        return self.__messages

    @property
    def message_count(self) -> int:
        """
        Gets the received message count.
        """
        return len(self.__messages)

    def receive_message(self, message: MessageEnvelope, queue: IMessageQueue):
        """
        Receives incoming message from the queue.
        :param message: an incoming message
        :param queue: a queue where the message comes from

        See :class:`MessageEnvelope <pip_services3_messaging.queues.MessageEnvelope.MessageEnvelope>`,
        class:`IMessageQueue <pip_services3_messaging.queues.IMessageQueue.IMessageQueue>`
        """
        with self.__lock:
            self.__messages.append(message)

    def clear(self, correlation_id: Optional[str]):
        """
        Clears all received messagers.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        with self.__lock:
            self.__messages = []
