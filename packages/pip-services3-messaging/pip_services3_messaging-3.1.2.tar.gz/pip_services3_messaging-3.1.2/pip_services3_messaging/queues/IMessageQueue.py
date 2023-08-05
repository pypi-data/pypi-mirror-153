# -*- coding: utf-8 -*-
"""
    pip_services3_messaging.queues.IMessageQeueue
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for message queues.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from typing import Optional, Any, List

from pip_services3_commons.run import IOpenable, IClosable

from pip_services3_messaging.queues import MessagingCapabilities, IMessageReceiver
from pip_services3_messaging.queues.MessageEnvelope import MessageEnvelope


class IMessageQueue(IOpenable, IClosable):
    """
    Interface for asynchronous message queues.

    Not all queues may implement all the methods.
    Attempt to call non-supported method will result in NotImplemented exception.
    To verify if specific method is supported consult with :class:`MessagingCapabilities <pip_services3_messaging.queues.MessagingCapabilities.MessagingCapabilities>`.

    See :class:`MessagingCapabilities <pip_services3_messaging.queues.MessagingCapabilities.MessagingCapabilities>`,
    :class:`MessageEnvelope <pip_services3_messaging.queues.MessageEnvelope.MessageEnvelope>`
    """

    def get_name(self) -> str:
        """
        Gets the queue name

        :return: the queue name.
        """
        raise NotImplementedError('Method from interface definition')

    def get_capabilities(self) -> MessagingCapabilities:
        """
        Gets the queue capabilities

        :return: the queue's capabilities object.
        """
        raise NotImplementedError('Method from interface definition')

    def read_message_count(self) -> int:
        """
        Reads the current number of messages in the queue to be delivered.

        :return: a number of messages
        """
        raise NotImplementedError('Method from interface definition')

    def send(self, correlation_id: Optional[str], envelop: MessageEnvelope):
        """
        Sends a message into the queue.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param envelop: a message envelop to be sent.
        """
        raise NotImplementedError('Method from interface definition')

    def send_as_object(self, correlation_id: Optional[str], message_type: str, message: Any):
        """
        Sends an object into the queue.
        Before sending the object is converted into JSON string and wrapped in a :class:`MessageEnvelope <pip_services3_messaging.MessageEnvelope.MessageEnvelope>`.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param message_type: a message type

        :param message: an object value to be sent
        """
        raise NotImplementedError('Method from interface definition')

    def peek(self, correlation_id: Optional[str]) -> MessageEnvelope:
        """
        Peeks a single incoming message from the queue without removing it.
        If there are no messages available in the queue it returns null.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :return: a message object.
        """
        raise NotImplementedError('Method from interface definition')

    def peek_batch(self, correlation_id: Optional[str], message_count: int) -> List[MessageEnvelope]:
        """
        Peeks multiple incoming messages from the queue without removing them.
        If there are no messages available in the queue it returns an empty list.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param message_count: a maximum number of messages to peek.

        :return: a list of message objects.
        """
        raise NotImplementedError('Method from interface definition')

    def receive(self, correlation_id: Optional[str], wait_timeout: int) -> MessageEnvelope:
        """
        Receives an incoming message and removes it from the queue.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param wait_timeout: a timeout in milliseconds to wait for a message to come.

        :return: a message object.
        """
        raise NotImplementedError('Method from interface definition')

    def renew_lock(self, message: MessageEnvelope, lock_timeout: int):
        """
        Renews a lock on a message that makes it invisible from other receivers in the queue.
        This method is usually used to extend the message processing time.

        :param message: a message to extend its lock.

        :param lock_timeout: a locking timeout in milliseconds.
        """
        raise NotImplementedError('Method from interface definition')

    def complete(self, message: MessageEnvelope):
        """
        Permanently removes a message from the queue.
        This method is usually used to remove the message after successful processing.

        :param message: a message to remove.
        """
        raise NotImplementedError('Method from interface definition')

    def abandon(self, message: MessageEnvelope):
        """
        Returnes message into the queue and makes it available for all subscribers to receive it again.
        This method is usually used to return a message which could not be processed at the moment
        to repeat the attempt. Messages that cause unrecoverable errors shall be removed permanently
        or/and send to dead letter queue.

        :param message: a message to return.
        """
        raise NotImplementedError('Method from interface definition')

    def move_to_dead_letter(self, message: MessageEnvelope):
        """
        Permanently removes a message from the queue and sends it to dead letter queue.

        :param message: a message to be removed.
        """
        raise NotImplementedError('Method from interface definition')

    def listen(self, correlation_id: Optional[str], receiver: IMessageReceiver):
        """
        Listens for incoming messages and blocks the current thread until queue is closed.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param receiver: a receiver to receive incoming messages.
        """
        raise NotImplementedError('Method from interface definition')

    def begin_listen(self, correlation_id: Optional[str], receiver: IMessageReceiver):
        """
        Listens for incoming messages without blocking the current thread.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param receiver: a receiver to receive incoming messages.
        """
        raise NotImplementedError('Method from interface definition')

    def end_listen(self, correlation_id: Optional[str]):
        """
        Ends listening for incoming messages.
        When this method is call :func:`listen` unblocks the thread and execution continues.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        raise NotImplementedError('Method from interface definition')
