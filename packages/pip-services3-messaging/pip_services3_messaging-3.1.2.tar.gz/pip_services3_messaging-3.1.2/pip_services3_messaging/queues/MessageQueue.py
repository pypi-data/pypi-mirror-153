# -*- coding: utf-8 -*-
"""
    pip_services3_messaging.queues.MessageQeueue
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Abstract message queue implementation.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import threading
from abc import abstractmethod
from typing import Optional, List, Any

from pip_services3_commons.config import IConfigurable, NameResolver, ConfigParams
from pip_services3_commons.errors import InvalidStateException
from pip_services3_commons.refer import IReferenceable, IReferences
from pip_services3_components.auth import CredentialResolver, CredentialParams
from pip_services3_components.connect import ConnectionResolver, ConnectionParams
from pip_services3_components.count import CompositeCounters
from pip_services3_components.log import CompositeLogger

from .IMessageQueue import IMessageQueue
from .IMessageReceiver import IMessageReceiver
from .MessageEnvelope import MessageEnvelope
from .MessagingCapabilities import MessagingCapabilities


class MessageQueue(IConfigurable, IReferenceable, IMessageQueue):
    """
    Abstract message queue.

    Abstract message queue that is used as a basis for specific message queue implementations.

    ### Configuration parameters ###
        - name:                        name of the message queue
        - connection(s):
            - discovery_key:             key to retrieve parameters from discovery service
            - protocol:                  connection protocol like http, https, tcp, udp
            - host:                      host name or IP address
            - port:                      port number
            - uri:                       resource URI or connection string with all parameters in it
        - credential(s):
        - store_key:                 key to retrieve parameters from credential store
        - username:                  user name
        - password:                  user password
        - access_id:                 application access id
        - access_key:                application secret key

    ### References ###
        - `*:logger:*:*:1.0`              (optional) :class:`ILogger <pip_services3_components.log.ILogger.ILogger>` components to pass log messages
        - `*:counters:*:*:1.0`            (optional) :class:`ICounters <pip_services3_components.count.ICounters.ICounters>` components to pass collected measurements
        - `*:discovery:*:*:1.0`           (optional) :class:`IDiscovery <pip_services3_components.connect.IDiscovery.IDiscovery>` components to discover connection(s)
        - `*:credential-store:*:*:1.0`    (optional) :class:`ICredentialStore <pip_services3_components.auth.ICredentialStore.ICredentialStore>` componetns to lookup credential(s)
    """

    def __init__(self, name: str = None, capabilities: MessagingCapabilities = None):
        """
        Creates a new instance of the message queue.

        :param name: (optional) a queue name
        :param capabilities: (optional) a capabilities of this message queue
        """
        self._lock: threading.Lock = threading.Lock()
        self._event = threading.Event()
        self._capabilities: MessagingCapabilities = None
        self._logger: CompositeLogger = CompositeLogger()
        self._counters: CompositeCounters = CompositeCounters()
        self._connection_resolver: ConnectionResolver = ConnectionResolver()
        self._credential_resolver: CredentialResolver = CredentialResolver()
        self._name: str = name
        self._capabilities = capabilities or \
                             MessagingCapabilities(False, False, False, False, False, False, False, False, False)

    def configure(self, config: ConfigParams):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        self._name = NameResolver.resolve(config)
        self._logger.configure(config)
        self._credential_resolver.configure(config)
        self._connection_resolver.configure(config)

    def set_references(self, references: IReferences):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        self._logger.set_references(references)
        self._counters.set_references(references)
        self._credential_resolver.set_references(references)
        self._connection_resolver.set_references(references)

    @abstractmethod
    def is_open(self) -> bool:
        """
        Checks if the component is opened.

        :return: true if the component has been opened and false otherwise.
        """

    def open(self, correlation_id: Optional[str]):
        """
        Opens the component.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        connection = self._connection_resolver.resolve_all(correlation_id)
        credential = self._credential_resolver.lookup(correlation_id)
        self._open_with_params(correlation_id, connection, credential)

    def _open_with_params(self, correlation_id: Optional[str], connections: List[ConnectionParams],
                          credential: CredentialParams):
        """
        Opens the component with given connection and credential parameters.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param connections: connection parameters

        :param credential: credential parameters
        """
        raise NotImplementedError('Abstract method that shall be overriden')

    def _check_open(self, correlation_id: Optional[str]):
        """
        Checks if the queue has been opened and throws an exception is it's not.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        if not self.is_open():
            raise InvalidStateException(
                correlation_id,
                "NOT_OPENED",
                "The queue is not opened"
            )

    def get_name(self) -> str:
        """
        Gets the queue name

        :return: the queue name.
        """
        return self._name if self._name is not None else "undefined"

    def get_capabilities(self) -> MessagingCapabilities:
        """
        Gets the queue capabilities

        :return: the queue's capabilities object.
        """
        return self._capabilities

    def send_as_object(self, correlation_id: Optional[str], message_type: str, message: Any):
        """
        Sends an object into the queue.
        Before sending the object is converted into JSON string and wrapped in a :class:`MessageEnvelope <pip_services3_messaging.MessageEnvelope.MessageEnvelope>`.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param message_type: a message type

        :param message: an object value to be sent
        """
        envelop = MessageEnvelope(correlation_id, message_type, message)
        self.send(correlation_id, envelop)

    def begin_listen(self, correlation_id: Optional[str], receiver: IMessageReceiver):
        """
        Listens for incoming messages without blocking the current thread.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param receiver: a receiver to receive incoming messages.
        """
        # Start listening on a parallel tread
        thread = threading.Thread(target=self.listen, args=(correlation_id, receiver))
        thread.daemon = True
        thread.start()

    def to_string(self) -> str:
        """
        Gets a string representation of the object.

        :return: a string representation of the object.
        """
        return "[" + self.get_name() + "]"

    def __str__(self):
        """
        Gets a string representation of the object.

        :return: a string representation of the object.
        """
        return self.to_string()

    @abstractmethod
    def close(self, correlation_id: Optional[str]):
        """
        Closes component and frees used resources.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """

    @abstractmethod
    def clear(self, correlation_id: Optional[str]):
        """
        Clears component state.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """

    @abstractmethod
    def read_message_count(self) -> int:
        """
        Reads the current number of messages in the queue to be delivered.

        :return: a number of messages in the queue.
        """

    @abstractmethod
    def send(self, correlation_id: Optional[str], envelop: MessageEnvelope):
        """
        Sends a message into the queue.
        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param envelop: a message envelop to be sent.
        """

    @abstractmethod
    def peek(self, correlation_id: Optional[str]) -> MessageEnvelope:
        """
        Peeks a single incoming message from the queue without removing it.
        If there are no messages available in the queue it returns `None`.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :return: a peeked message or `None`.
        """

    @abstractmethod
    def peek_batch(self, correlation_id: Optional[str], message_count: int) -> List[MessageEnvelope]:
        """
        Peeks multiple incoming messages from the queue without removing them.
        If there are no messages available in the queue it returns an empty list.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param message_count: a maximum number of messages to peek.
        :return: a list of peeked messages
        """

    @abstractmethod
    def receive(self, correlation_id: Optional[str], wait_timeout: int) -> MessageEnvelope:
        """

        Receives an incoming message and removes it from the queue.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param wait_timeout: a timeout in milliseconds to wait for a message to come.
        :return: a received message or `None`.
        """

    @abstractmethod
    def renew_lock(self, message: MessageEnvelope, lock_timeout: int):
        """
        Renews a lock on a message that makes it invisible from other receivers in the queue.
        This method is usually used to extend the message processing time.

        :param message: a message to extend its lock.
        :param lock_timeout: a locking timeout in milliseconds.
        """

    @abstractmethod
    def complete(self, message: MessageEnvelope):
        """
        Permanently removes a message from the queue.
        This method is usually used to remove the message after successful processing.
        :param message: a message to remove.
        """

    @abstractmethod
    def abandon(self, message: MessageEnvelope):
        """
        Returnes message into the queue and makes it available for all subscribers to receive it again.
        This method is usually used to return a message which could not be processed at the moment
        to repeat the attempt. Messages that cause unrecoverable errors shall be removed permanently
        or/and send to dead letter queue.

        :param message: a message to return.
        """

    @abstractmethod
    def move_to_dead_letter(self, message: MessageEnvelope):
        """
        Permanently removes a message from the queue and sends it to dead letter queue.

        :param message: a message to be removed.
        """

    @abstractmethod
    def listen(self, correlation_id: Optional[str], receiver: IMessageReceiver):
        """
        Listens for incoming messages and blocks the current thread until queue is closed.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param receiver: a receiver to receive incoming messages.
        """

    @abstractmethod
    def end_listen(self, correlation_id: Optional[str]):
        """
        Ends listening for incoming messages.
        When this method is call **listen** unblocks the thread and execution continues.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
