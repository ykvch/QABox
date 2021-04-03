"""The most basic example of message passing via RabbitMQ"""

import pika
import pytest

BROKER = "localhost"
QUEUE = "hello"
BODY = "Hello World!"


@pytest.fixture
def broker():
    pass


@pytest.fixture
def pub():
    connection = pika.BlockingConnection(pika.ConnectionParameters(BROKER))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE)
    yield channel
    connection.close()


@pytest.fixture
def sub():
    conn = pika.BlockingConnection(pika.ConnectionParameters(BROKER))
    channel = conn.channel()
    channel.queue_declare(queue=QUEUE)
    yield channel
    conn.close()


def test_basic_get(pub, sub):
    # messages = []

    # sub.basic_consume(
    #     queue=QUEUE,
    #     auto_ack=True,
    #     on_message_callback=lambda c, m, p, b: messages.append(b))

    pub.basic_publish(exchange="", routing_key=QUEUE, body=BODY)

    # sub.start_consuming()
    # assert messages.pop() == BODY

    msg = sub.basic_get(QUEUE)
    assert msg[-1].decode() == BODY
