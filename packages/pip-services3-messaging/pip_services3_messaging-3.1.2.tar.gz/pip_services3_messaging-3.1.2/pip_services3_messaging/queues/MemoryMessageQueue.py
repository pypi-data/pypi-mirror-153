# -*- coding: utf-8 -*-
"""
    pip_services3_messaging.queues.MemoryMessageQueue
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Memory message queue implementation.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
import datetime
import threading
from typing import List, Optional

from pip_services3_commons.config import ConfigParams
from pip_services3_commons.run import ICleanable
from pip_services3_components.auth import CredentialParams
from pip_services3_components.connect import ConnectionParams

from .IMessageReceiver import IMessageReceiver
from .LockedMessage import LockedMessage
from .MessageEnvelope import MessageEnvelope
from .MessageQueue import MessageQueue
from .MessagingCapabilities import MessagingCapabilities


class MemoryMessageQueue(MessageQueue, ICleanable):
    """
    Message queue that sends and receives messages within the same process by using shared memory.
    This queue is typically used for testing to mock real queues.

    ### Configuration parameters ###
        - name:                        name of the message queue

    ### References ###
        - `*:logger:*:*:1.0`           (optional) :class:`ILogger <pip_services3_components.log.ILogger.ILogger>` components to pass log messages
        - `*:counters:*:*:1.0`         (optional) :class:`ICounters <pip_services3_components.count.ICounters.ICounters>` components to pass collected measurements

    Example:

    .. code-block:: python

        queue = MessageQueue("myqueue")
        queue.send("123", MessageEnvelope(None, "mymessage", "ABC"))

        message = queue.receive("123", 0)
        if message != None:
            # ...
            queue.complete("123", message)
    """

    def __init__(self, name: str = None):
        """
        Creates a new instance of the message queue.

        :param name: (optional) a queue name.
        """
        super(MemoryMessageQueue, self).__init__(name)
        self._event = threading.Event()
        self._capabilities = MessagingCapabilities(True, True, True, True, True, True, True, False, True)

        self.__messages: List[MessageEnvelope] = []
        self.__locked_messages: dict = {}
        self.__opened = False
        # Used to stop the listening process.
        self.__cancel = False
        self.__lock_token_sequence = 0
        self.__listen_interval = 1000

    def is_open(self) -> bool:
        """
        Checks if the component is opened.

        :return: true if the component has been opened and false otherwise.
        """
        return self.__opened

    def _open_with_params(self, correlation_id: Optional[str], connections: List[ConnectionParams],
                          credentials: CredentialParams):
        """
        Opens the component with given connection and credential parameters.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param connections: connection parameters

        :param credentials: credential parameters
        """
        self.__opened = True
        self._logger.trace(correlation_id, "Opened queue " + str(self))

    def close(self, correlation_id: Optional[str]):
        """
        Closes component and frees used resources.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        with self._lock:
            self.__opened = False
            self.__cancel = True
            self._event.set()

        self._logger.trace(correlation_id, "Closed queue " + str(self))

    def clear(self, correlation_id: Optional[str]):
        """
        Clears component state.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        with self._lock:
            # Clear messages
            self.__messages = []
            self.__locked_messages = {}
            self.__cancel = False

        self._logger.trace(correlation_id, "Cleared queue " + str(self))

    def configure(self, config: ConfigParams):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        super().configure(config)

        self.__listen_interval = config.get_as_integer_with_default('listen_interval', self.__listen_interval)
        self.__listen_interval = config.get_as_integer_with_default('options.listen_interval', self.__listen_interval)

    def read_message_count(self) -> int:
        """
        Reads the current number of messages in the queue to be delivered.

        :return: a number of messages
        """
        with self._lock:
            return len(self.__messages)

    def send(self, correlation_id: Optional[str], message: MessageEnvelope):
        """
        Sends a message into the queue.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param message: a message envelop to be sent.
        """
        if message is None: return
        message.sent_time = datetime.datetime.now()

        with self._lock:
            # Add message to the queue
            self.__messages.append(message)

            # Release threads waiting for messages
            self._event.set()

        self._counters.increment_one("queue." + self.get_name() + ".sent_messages")
        self._logger.debug(correlation_id, "Sent message " + str(message) + " via " + str(self))

    def peek(self, correlation_id: Optional[str]) -> MessageEnvelope:
        """
        Peeks a single incoming message from the queue without removing it.
        If there are no messages available in the queue it returns null.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :return: a message object.
        """
        message = None

        with self._lock:
            # Pick a message
            if len(self.__messages) > 0:
                message = self.__messages[0]

        if message is not None:
            self._logger.trace(correlation_id, "Peeked message " + str(message) + " on " + str(self))

        return message

    def peek_batch(self, correlation_id: Optional[str], message_count: int) -> List[MessageEnvelope]:
        """
        Peeks multiple incoming messages from the queue without removing them.
        If there are no messages available in the queue it returns an empty list.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param message_count: a maximum number of messages to peek.

        :return: a list of message objects.
        """
        messages = []
        with self._lock:
            messages = self.__messages[:message_count]

        self._logger.trace(correlation_id, "Peeked " + str(len(messages)) + " messages on " + str(self))

        return messages

    def receive(self, correlation_id: Optional[str], wait_timeout: int) -> Optional[MessageEnvelope]:
        """
        Receives an incoming message and removes it from the queue.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param wait_timeout: a timeout in milliseconds to wait for a message to come.

        :return: a message object.
        """
        check_interval_ms = 100
        elapsed_time = 0
        message = None

        with self._lock:
            # Get message the the queue

            if len(self.__messages) > 0:
                message = self.__messages.pop(0)

        while elapsed_time < wait_timeout and message is None:
            # Wait for a while
            self._event.wait(check_interval_ms / 1000)
            elapsed_time += check_interval_ms

            with self._lock:
                # Get message the the queue
                if len(self.__messages) > 0:
                    message = self.__messages.pop(0)

        if message is None:
            return message

        # Generate and set locked token
        locked_token = self.__lock_token_sequence
        self.__lock_token_sequence += 1
        message.set_reference(locked_token)

        # Add messages to locked messages list
        locked_message = LockedMessage()
        now = datetime.datetime.now()
        locked_message.expiration_time = datetime.datetime.fromtimestamp(now.timestamp() + wait_timeout / 1000)
        locked_message.message = message
        locked_message.timeout = wait_timeout
        self.__locked_messages[locked_token] = locked_message

        # Instrument the process
        self._counters.increment_one("queue." + self.get_name() + ".received_messages")
        self._logger.debug(message.correlation_id, "Received message " + str(message) + " on " + str(self))

        return message

    def renew_lock(self, message: MessageEnvelope, lock_timeout: int):
        """
        Renews a lock on a message that makes it invisible from other receivers in the queue.
        This method is usually used to extend the message processing time.

        :param message: a message to extend its lock.

        :param lock_timeout: a locking timeout in milliseconds.
        """
        if message.get_reference() is None:
            return

        with self._lock:
            # Get message from locked queue
            locked_token = message.get_reference()
            locked_message = self.__locked_messages[locked_token]
            now = datetime.datetime.now()
            # If lock is found, extend the lock
            if locked_message.expiration_time > now:
                locked_message.expiration_time = now.timestamp() + locked_message.timeout / 1000

        self._logger.trace(message.correlation_id, "Renewed lock for message " + str(message) + " at " + str(self))

    def abandon(self, message: MessageEnvelope):
        """
        Returnes message into the queue and makes it available for all subscribers to receive it again.
        This method is usually used to return a message which could not be processed at the moment
        to repeat the attempt. Messages that cause unrecoverable errors shall be removed permanently
        or/and send to dead letter queue.

        :param message: a message to return.
        """
        if message.get_reference() is None:
            return

        with self._lock:
            # Get message from locked queue
            locked_token = message.get_reference()
            locked_message = self.__locked_messages[locked_token]
            if locked_message is not None:
                # Remove from locked messages
                del self.__locked_messages[locked_token]
                message.set_reference(None)

                # Skip if it is already expired
                if locked_message.expiration_time <= datetime.datetime.now():
                    return
            # Skip if it absent
            else:
                return

        self._logger.trace(message.correlation_id, "Abandoned message " + str(message) + " at " + str(self))

        # Add back to the queue
        self.send(message.correlation_id, message)

    def complete(self, message: MessageEnvelope):
        """
        Permanently removes a message from the queue.
        This method is usually used to remove the message after successful processing.

        :param message: a message to remove.
        """
        if message.get_reference() is None:
            return

        with self._lock:
            lock_key = message.get_reference()
            del self.__locked_messages[lock_key]
            message.set_reference(None)

        self._logger.trace(message.correlation_id, "Completed message " + str(message) + " at " + str(self))

    def move_to_dead_letter(self, message: MessageEnvelope):
        """
        Permanently removes a message from the queue and sends it to dead letter queue.

        :param message: a message to be removed.
        """
        if message.get_reference() is None:
            return

        with self._lock:
            lock_key = message.get_reference()
            del self.__locked_messages[lock_key]
            message.set_reference(None)

        self._counters.increment_one("queue." + self.get_name() + ".dead_messages")
        self._logger.trace(message.correlation_id, "Moved to dead message " + str(message) + " at " + str(self))

    def listen(self, correlation_id: Optional[str], receiver: IMessageReceiver):
        """
        Listens for incoming messages and blocks the current thread until queue is closed.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param receiver: a receiver to receive incoming messages.
        """
        timeout_interval = self.__listen_interval

        self._logger.trace(correlation_id, "Started listening messages at " + str(self))

        with self._lock:
            self.__cancel = False

        while not self.__cancel:
            try:
                message = self.receive(correlation_id, timeout_interval)
                if message is not None and not self.__cancel:
                    receiver.receive_message(message, self)
            except Exception as ex:
                self._logger.error(correlation_id, ex, "Failed to process the message")

    def end_listen(self, correlation_id: Optional[str]):
        """
        Ends listening for incoming messages.
        When this method is call :func:`listen` unblocks the thread and execution continues.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        with self._lock:
            self.__cancel = True
