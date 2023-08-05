# -*- coding: utf-8 -*-
import time

from pip_services3_commons.data import IdGenerator
from pip_services3_commons.random import RandomString

from pip_services3_messaging.queues import IMessageQueue, MessageEnvelope
from pip_services3_messaging.test.TestMessageReceiver import TestMessageReceiver


class MessageQueueFixture:
    def __init__(self, queue: IMessageQueue):
        self.__queue: IMessageQueue = queue

    def test_send_receive_message(self):
        envelope1 = MessageEnvelope("123", "Test", "Test message")
        self.__queue.send(None, envelope1)

        envelope2 = self.__queue.receive(None, 10000)
        assert envelope2 is not None
        assert envelope1.message_type == envelope2.message_type
        assert envelope1.message == envelope2.message
        assert envelope1.correlation_id == envelope2.correlation_id

    def test_receive_send_message(self):
        envelope1 = MessageEnvelope("123", "Test", "Test message")

        time.sleep(0.5)
        self.__queue.send(None, envelope1)

        envelope2 = self.__queue.receive(None, 10000)
        assert envelope2 is not None
        assert envelope1.message_type == envelope2.message_type
        assert envelope1.message == envelope2.message
        assert envelope1.correlation_id == envelope2.correlation_id

    def test_receive_complete_message(self):
        envelope1 = MessageEnvelope("123", "Test", "Test message")

        self.__queue.send(None, envelope1)

        count = self.__queue.read_message_count()
        assert count > 0

        envelope2 = self.__queue.receive(None, 10000)
        assert envelope2 is not None
        assert envelope1.message_type == envelope2.message_type
        assert envelope1.message == envelope2.message
        assert envelope1.correlation_id == envelope2.correlation_id

        self.__queue.complete(envelope2)
        assert envelope2.get_reference() is None

    def test_receive_abandon_message(self):
        envelope1 = MessageEnvelope("123", "Test", "Test message")
        self.__queue.send(None, envelope1)

        envelope2 = self.__queue.receive(None, 10000)
        assert envelope2 is not None
        assert envelope1.message_type == envelope2.message_type
        assert envelope1.message == envelope2.message
        assert envelope1.correlation_id == envelope2.correlation_id

        self.__queue.abandon(envelope2)

        envelope2 = self.__queue.receive(None, 10000)
        assert envelope2 is not None
        assert envelope1.message_type == envelope2.message_type
        assert envelope1.message == envelope2.message
        assert envelope1.correlation_id == envelope2.correlation_id

    def test_send_peek_message(self):
        envelope1 = MessageEnvelope("123", "Test", "Test message")
        self.__queue.send(None, envelope1)

        envelope2 = self.__queue.peek(None)
        assert envelope2 is not None
        assert envelope1.message_type == envelope2.message_type
        assert envelope1.message == envelope2.message
        assert envelope1.correlation_id == envelope2.correlation_id

    def test_peek_no_message(self):
        envelope = self.__queue.peek(None)
        assert envelope is None

    def test_move_dead_message(self):
        envelope1 = MessageEnvelope("123", "Test", "Test message")
        self.__queue.send(None, envelope1)

        envelope2 = self.__queue.receive(None, 10000)
        assert envelope2 is not None
        assert envelope1.message_type == envelope2.message_type
        assert envelope1.message == envelope2.message
        assert envelope1.correlation_id == envelope2.correlation_id

        self.__queue.move_to_dead_letter(envelope2)

    def test_on_message(self):
        message_receiver = TestMessageReceiver()
        self.__queue.begin_listen(None, message_receiver)

        time.sleep(1)

        envelope1 = MessageEnvelope("123", "Test", "Test message")
        self.__queue.send(None, envelope1)

        time.sleep(1)

        envelope2 = message_receiver.messages[0]
        assert envelope2 is not None
        assert envelope1.message_type == envelope2.message_type
        assert envelope1.message == envelope2.message
        assert envelope1.correlation_id == envelope2.correlation_id

        self.__queue.end_listen(None)

    def test_send_as_object(self):
        message_receiver = TestMessageReceiver()
        test_obj = {
            'id': IdGenerator.next_long(),
            'name': RandomString.next_string(20, 50)
        }

        self.__queue.begin_listen(None, message_receiver)

        time.sleep(1)
        # send array of strings
        self.__queue.send_as_object('123', 'messagetype', ['string1', 'string2'])
        time.sleep(1)

        assert message_receiver.message_count == 1
        envelope = message_receiver.messages[0]
        assert envelope is not None
        assert 'messagetype' == envelope.message_type
        assert '123' == envelope.correlation_id

        message = envelope.get_message_as()
        assert isinstance(message, list)
        assert 'string1' in message and 'string2' in message

        # send string
        message_receiver.clear(None)
        self.__queue.send_as_object('123', 'messagetype', 'string2')

        time.sleep(1)

        assert 1 == message_receiver.message_count
        envelope = message_receiver.messages[0]
        assert envelope is not None
        assert 'messagetype' == envelope.message_type
        assert '123' == envelope.correlation_id

        message2 = envelope.get_message_as_string()
        assert 'string2' == message2

        self.__queue.end_listen(None)
