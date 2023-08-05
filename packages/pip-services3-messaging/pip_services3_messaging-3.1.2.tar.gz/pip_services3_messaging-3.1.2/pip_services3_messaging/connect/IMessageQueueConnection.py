# -*- coding: utf-8 -*-
from abc import ABC
from typing import List


class IMessageQueueConnection(ABC):
    """
    Defines an interface for message queue connections
    """

    def read_queue_names(self) -> List[str]:
        """
        Reads a list of registered queue names.
        If connection doesn't support this function returnes an empty list.

        :return: a list with registered queue names.
        """

    def create_queue(self, name: str):
        """
        Creates a message queue.
        If connection doesn't support this function it exists without error.

        :param name: the name of the queue to be created.
        """

    def delete_queue(self, name: str):
        """
        Deletes a message queue.
        If connection doesn't support this function it exists without error.

        :param name: the name of the queue to be deleted.
        """
