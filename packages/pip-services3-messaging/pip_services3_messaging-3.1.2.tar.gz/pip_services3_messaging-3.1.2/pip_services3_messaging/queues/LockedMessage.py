# -*- coding: utf-8 -*-
import datetime

from pip_services3_messaging.queues import MessageEnvelope


class LockedMessage:
    """
    Data object used to store and lock incoming messages
    in :class:`MemoryMessageQueue <pip_services3_messaging.queues.MemoryMessageQueue.MemoryMessageQueue>`.

    See :class:`MemoryMessageQueue <pip_services3_messaging.queues.MemoryMessageQueue.MemoryMessageQueue>`
    """

    def __init__(self):
        # The incoming message.
        self.message: MessageEnvelope = None
        # The expiration time for the message lock.
        # If it is null then the message is not locked.
        self.expiration_time: datetime.datetime = None
        # The lock timeout in milliseconds.
        self.timeout: int = None
