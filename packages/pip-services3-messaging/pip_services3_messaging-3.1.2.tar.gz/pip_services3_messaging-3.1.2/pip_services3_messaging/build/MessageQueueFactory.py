# -*- coding: utf-8 -*-
from abc import abstractmethod

from pip_services3_commons.config import IConfigurable, ConfigParams
from pip_services3_commons.refer import IReferenceable, IReferences
from pip_services3_components.build import Factory

from pip_services3_messaging.build.IMessageQueueFactory import IMessageQueueFactory
from pip_services3_messaging.queues import IMessageQueue


class MessageQueueFactory(Factory, IMessageQueueFactory, IConfigurable, IReferenceable):
    """
    Creates :class:`IMessageQueue <pip_services3_messaging.queues.IMessageQueue.IMessageQueue>`. components by their descriptors.
    Name of created message queue is taken from its descriptor.

    See :class:`Factory <pip_services3_components.build.Factory.Factory>`,
    :class:`MessageQueue <pip_services3_messaging.queues.MessageQueue.MessageQueue>`
    """

    def __init__(self):
        super().__init__()
        self._config: ConfigParams = None
        self._references: IReferences = None

    def configure(self, config: ConfigParams):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        self._config = config

    def set_references(self, references: IReferences):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        self._references = references

    @abstractmethod
    def create_queue(self, name: str) -> IMessageQueue:
        """
        Creates a message queue component and assigns its name.
        :param name: a name of the created message queue.
        :return: IMessageQueue instance
        """
