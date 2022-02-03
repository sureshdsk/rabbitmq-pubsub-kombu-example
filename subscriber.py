from kombu import Connection, Exchange, Queue, binding
from kombu.mixins import ConsumerMixin
import sys
from functools import partial


class Worker(ConsumerMixin):
    def __init__(self, connection, queue):
        self.connection = connection
        self.queue = queue

    def get_consumers(self, Consumer, channel):
        return [
            Consumer(
                queues=[self.queue],
                callbacks=[partial(self.on_message, self.queue.name)],
            )
        ]

    def on_message(
        self,
        queue_name,
        body,
        message,
    ):
        print("{}: got message: {}".format(queue_name, body))
        message.ack()


queue_name, routing_key = sys.argv[1:]


rabbit_url = "amqp://localhost:6672/"

with Connection(
    rabbit_url, heartbeat=4, userid="admin", password="localmq012345"
) as conn:
    try:
        exchange = Exchange("example-topic-exchange", type="topic")
        queue = Queue(
            name=queue_name,
            exchange=exchange,
            type="topic",
            routing_key=routing_key,
        )
        queue.maybe_bind(conn)
        queue.declare()

        worker = Worker(conn, queue)
        worker.run()
    except KeyboardInterrupt:
        print("Terminated")
    except:
        raise
