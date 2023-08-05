# -*- coding: utf-8 -*-
"""
    pip_services3_messaging.build.DefaultMessagingFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    DefaultMessagingFactory  implementation

    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from pip_services3_commons.refer import Descriptor
from pip_services3_components.build import Factory

from .MemoryMessageQueueFactory import MemoryMessageQueueFactory
from ..queues.MemoryMessageQueue import MemoryMessageQueue


class DefaultMessagingFactory(Factory):
    """
    Creates :class:`MemoryMessageQueue <pip_services3_messaging.queues.MemoryMessageQueue.MemoryMessageQueue>` components by their descriptors.
    Name of created message queue is taken from its descriptor.
    """
    MemoryMessageQueueDescriptor = Descriptor("pip-services", "message-queue", "memory", "*", "*")
    MemoryMessageQueueFactoryDescriptor = Descriptor("pip-services", "factory", "message-queue", "memory", "1.0")

    def __init__(self):
        """
        Create a new instance of the factory.
        """

        super().__init__()
        self.register(DefaultMessagingFactory.MemoryMessageQueueDescriptor,
                      lambda locator: MemoryMessageQueue(
                          None if not callable(locator.get_name) else locator.get_name()
                      ))
        self.register_as_type(DefaultMessagingFactory.MemoryMessageQueueFactoryDescriptor, MemoryMessageQueueFactory)

