import json
from kombu import Connection, Exchange, Queue, Producer

rabbit_url = "amqp://localhost:6672/"

conn = Connection(rabbit_url, userid="admin", password="localmq012345")

channel = conn.channel()

exchange = Exchange("example-topic-exchange", type="topic")

queue = Queue(
    name="example-topic", exchange=exchange, type="topic", routing_key="app.user.invited"
)
queue.maybe_bind(conn)
queue.declare()

queue2 = Queue(
    name="example-topic2", exchange=exchange, type="topic", routing_key="app.user.invited"
)
queue2.maybe_bind(conn)
queue2.declare()

queue3 = Queue(
    name="example-topic3", exchange=exchange, type="topic", routing_key="app.user.made_admin"
)
queue3.maybe_bind(conn)
queue3.declare()


queue4 = Queue(
    name="example-topic4", exchange=exchange, type="topic", routing_key="app.user.*"
)
queue4.maybe_bind(conn)
queue4.declare()


events = [
    {"routing_key": "app.user.invited", "message": json.dumps({"user_id": 1001})},
    {"routing_key": "app.user.made_admin", "message": json.dumps({"user_id": 1001, "role":"admin"})},
]
for event in events:
    producer = Producer(exchange=exchange, channel=channel, routing_key=event["routing_key"])
    producer.publish(event["message"])
