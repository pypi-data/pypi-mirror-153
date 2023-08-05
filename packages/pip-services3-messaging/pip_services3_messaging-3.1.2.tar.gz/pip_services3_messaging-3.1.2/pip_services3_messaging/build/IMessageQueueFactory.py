# -*- coding: utf-8 -*-
from abc import ABC

from pip_services3_messaging.queues.IMessageQueue import IMessageQueue


class IMessageQueueFactory(ABC):
    """
    Creates message queue components.

    See :class:`IMessageQueue <pip_services3_messaging.queues.IMessageQueue.IMessageQueue>`.

    """

    def create_queue(self, name: str) -> IMessageQueue:
        """
        Creates a message queue component and assigns its name.

        :param name: a name of the created message queue.
        :return: IMessageQueue instance
        """
