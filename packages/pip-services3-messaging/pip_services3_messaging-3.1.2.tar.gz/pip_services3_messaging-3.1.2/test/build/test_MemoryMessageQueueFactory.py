# -*- coding: utf-8 -*-
from pip_services3_commons.refer import Descriptor

from pip_services3_messaging.build import MemoryMessageQueueFactory


class TestMemoryMessageQueueFactory:

    def test_create_message_queue(self):
        factory = MemoryMessageQueueFactory()
        descriptor = Descriptor("pip-services", "message-queue", "memory", "test", "1.0")

        can_result = factory.can_create(descriptor)
        assert can_result is not None

        queue = factory.create(descriptor)
        assert queue is not None
        assert queue.get_name() == 'test'
