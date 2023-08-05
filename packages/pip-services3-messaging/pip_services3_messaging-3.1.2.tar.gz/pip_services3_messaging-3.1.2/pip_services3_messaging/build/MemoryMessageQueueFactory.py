# -*- coding: utf-8 -*-
"""
    pip_services3_messaging.build.MemoryMessageQueueFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    MemoryMessageQueueFactory implementation

    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from pip_services3_commons.refer import Descriptor

from pip_services3_messaging.queues import IMessageQueue
from .MessageQueueFactory import MessageQueueFactory
from ..queues.MemoryMessageQueue import MemoryMessageQueue


class MemoryMessageQueueFactory(MessageQueueFactory):
    """
    Creates :class:`MemoryMessageQueue <pip_services3_messaging.queues.MemoryMessageQueue.MemoryMessageQueue>` components by their descriptors.
    Name of created message queue is taken from its descriptor.
    """

    MemoryQueueDescriptor = Descriptor("pip-services", "message-queue", "memory", "*", "*")

    def __init__(self):
        """
        Create a new instance of the factory.
        """
        super(MemoryMessageQueueFactory, self).__init__()

        self.register(MemoryMessageQueueFactory.MemoryQueueDescriptor,
                      lambda locator: self.create_queue(
                          None if not callable(locator.get_name) else locator.get_name()
                      ))

    def create_queue(self, name: str) -> IMessageQueue:
        """
        Creates a message queue component and assigns its name.

        :param name: a name of the created message queue.
        :return: IMessageQueue instance
        """
        queue = MemoryMessageQueue(name)

        if self._config is not None:
            queue.configure(self._config)

        if self._references is not None:
            queue.set_references(self._references)

        return queue
