# -*- coding: utf-8 -*-
"""
    pip_services3_messaging.queues.IMessageReceiver
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for message receivers.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from abc import ABC

from pip_services3_messaging.queues import IMessageQueue
from pip_services3_messaging.queues.MessageEnvelope import MessageEnvelope


class IMessageReceiver(ABC):
    """
    Callback interface to receive incoming messages.

    Example:

    .. code-block:: python

        class MyMessageReceiver(IMessageReceiver):
            def receive_message(self, envelop, queue):
                print "Received message: " + envelop.get_message_as_string()

        messageQueue = MemoryMessageQueue()
        messageQueue.listen("123", MyMessageReceiver())

        messageQueue.open("123")
        messageQueue.send("123", MessageEnvelope(None, "mymessage", "ABC")) # Output in console: "ABC"
    """

    def receive_message(self, message: MessageEnvelope, queue: IMessageQueue):
        """
        Receives incoming message from the queue.
        :param message: an incoming message
        :param queue: a queue where the message comes from

        See :class:`MessageEnvelope <pip_services3_messaging.queues.MessageEnvelope.MessageEnvelope>`,
        :class:`IMessageQueue <pip_services3_messaging.queues.IMessageQueue.IMessageQueue>`
        """
        raise NotImplementedError('Method from interface definition')
