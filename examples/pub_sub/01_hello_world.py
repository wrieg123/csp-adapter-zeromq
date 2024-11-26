import csp
import pytz
from datetime import datetime, timedelta

from csp_adapter_zeromq import PubSocket, SubSocket, ZeroMQAdapter


@csp.node
def publisher_node() -> csp.ts[str]:
    with csp.alarms():
        alarm: csp.ts[str] = csp.alarm(str)

    with csp.state():
        num_messages: int = 0

    with csp.start():
        csp.schedule_alarm(alarm, timedelta(seconds=1), f"Message #{num_messages}")

    if csp.ticked(alarm):
        num_messages += 1
        csp.schedule_alarm(alarm, timedelta(seconds=1), f"Message #{num_messages}")
        return alarm


@csp.node
def subscriber_node(messages: csp.ts[str], n: int) -> csp.ts[bool]:
    with csp.state():
        received_messages: int = 0

    if csp.ticked(messages):
        received_messages += 1
        if received_messages >= n:
            return True


@csp.graph
def g(n: int):
    adapter_manager = ZeroMQAdapter()

    # Bind the socket to the uri
    pub_socket: PubSocket = adapter_manager.pub(uri="tcp://*:5555", bind=True)

    # Connect to the socket
    sub_socket: SubSocket = adapter_manager.sub(uri="tcp://127.0.0.1:5555", connect=True)

    # Publish messages over
    published_messages = publisher_node()
    pub_socket.publish(topic="", edge=published_messages)
    csp.print("published", published_messages)

    # Subscribe to topics
    subscribed = sub_socket.subscribe("", str)

    csp.print("received", subscribed)

    # Stop the engine after a certain number of messages have been recieved on a topic
    csp.stop_engine(subscriber_node(subscribed, n))


csp.run(g, 5, starttime=datetime.now(pytz.UTC), endtime=timedelta(minutes=10), realtime=True)
