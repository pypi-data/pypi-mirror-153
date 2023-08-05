# -*- coding: utf-8 -*-
"""
    pip_services3_messaging.queues.MessagingCapabilities
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Messaging capabilities implementation.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""


class MessagingCapabilities:
    """
    Data object that contains supported capabilities of a message queue.
    If certain capability is not supported a queue will throw NotImplemented exception.
    """

    def __init__(self, can_message_count: bool, can_send: bool, can_receive: bool, can_peek: bool, can_peek_batch: bool,
                 can_renew_lock: bool,
                 can_abandon: bool, can_dead_letter: bool, can_clear: bool):
        """
        Creates a new instance of the capabilities object.

        :param can_message_count: true if queue supports reading message count.
        :param can_send: true if queue is able to send messages.
        :param can_receive: true if queue is able to receive messages.
        :param can_peek: true if queue is able to peek messages.
        :param can_peek_batch: true if queue is able to peek multiple messages in one batch.
        :param can_renew_lock: true if queue is able to renew message lock.
        :param can_abandon: true if queue is able to abandon messages.
        :param can_dead_letter: true if queue is able to send messages to dead letter queue.
        :param can_clear: true if queue can be cleared.
        """
        self._can_message_count = can_message_count
        self._can_send = can_send
        self._can_receive = can_receive
        self._can_peek = can_peek
        self._can_peek_batch = can_peek_batch
        self._can_renew_lock = can_renew_lock
        self._can_abandon = can_abandon
        self._can_dead_letter = can_dead_letter
        self._can_clear = can_clear

    @property
    def can_message_count(self) -> bool:
        """
        Informs if the queue is able to read number of messages.

        :return: true if queue supports reading message count.
        """
        return self._can_message_count

    @property
    def can_send(self) -> bool:
        """
        Informs if the queue is able to send messages.

        :return: true if queue is able to send messages.
        """
        return self._can_send

    @property
    def can_receive(self) -> bool:
        """
        Informs if the queue is able to receive messages.

        :return: true if queue is able to receive messages.
        """
        return self._can_receive

    @property
    def can_peek(self) -> bool:
        """
        Informs if the queue is able to peek messages.

        :return: true if queue is able to peek messages.
        """
        return self._can_peek

    @property
    def can_peek_batch(self) -> bool:
        """
        Informs if the queue is able to peek multiple messages in one batch.

        :return: true if queue is able to peek multiple messages in one batch.
        """
        return self._can_peek_batch

    @property
    def can_renew_lock(self) -> bool:
        """
        Informs if the queue is able to renew message lock.

        :return: true if queue is able to renew message lock.
        """
        return self._can_renew_lock

    @property
    def can_abandon(self) -> bool:
        """
        Informs if the queue is able to abandon messages.

        :return: true if queue is able to abandon.
        """
        return self._can_abandon

    @property
    def can_dead_letter(self) -> bool:
        """
        Informs if the queue is able to send messages to dead letter queue.

        :return: true if queue is able to send messages to dead letter queue.
        """
        return self._can_dead_letter

    @property
    def can_clear(self) -> bool:
        """
        Informs if the queue can be cleared.

        :return: true if queue can be cleared.
        """
        return self._can_clear
