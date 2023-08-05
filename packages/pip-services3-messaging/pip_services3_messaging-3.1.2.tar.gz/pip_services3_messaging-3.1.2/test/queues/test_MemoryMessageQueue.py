# -*- coding: utf-8 -*-
from pip_services3_messaging.queues import MemoryMessageQueue
from test.queues.MessageQueueFixture import MessageQueueFixture


class TestMemoryMessageQueue:
    queue: MemoryMessageQueue = None
    fixture: MessageQueueFixture = None

    @classmethod
    def setup_class(cls):
        cls.queue = MemoryMessageQueue("TestQueue")
        cls.fixture = MessageQueueFixture(cls.queue)
        cls.queue.open(None)

    @classmethod
    def teardown_class(cls):
        cls.queue.close(None)

    def setup_method(self):
        self.queue.clear(None)

    def test_send_receive_message(self):
        self.fixture.test_send_receive_message()

    def test_receive_send_message(self):
        self.fixture.test_receive_send_message()

    def test_receive_and_complete_message(self):
        self.fixture.test_receive_complete_message()

    def test_receive_and_abandon_message(self):
        self.fixture.test_receive_abandon_message()

    def test_send_peek_message(self):
        self.fixture.test_send_peek_message()

    def test_peek_no_message(self):
        self.fixture.test_peek_no_message()

    def test_move_to_dead_message(self):
        self.fixture.test_move_dead_message()

    def test_on_message(self):
        self.fixture.test_on_message()

    def test_send_message_as_object(self):
        self.fixture.test_send_as_object()
