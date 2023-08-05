# -*- coding: utf-8 -*-
import json

from pip_services3_messaging.queues import MessageEnvelope


class TestMessageEnvelop:
    def test_from_to_json(self):
        message = MessageEnvelope("123", "Test", "This is a test message")
        jsoon = json.dumps(message.to_json())

        message2 = MessageEnvelope.from_json(jsoon)
        assert message.message_id == message2.message_id
        assert message.correlation_id == message2.correlation_id
        assert message.message_type == message2.message_type
        assert message.message.decode('utf-8') == message2.message.decode('utf-8')
