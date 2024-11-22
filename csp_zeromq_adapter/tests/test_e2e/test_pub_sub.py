import csp
from csp import ts
from csp.adapters.utils import JSONTextMessageMapper
from datetime import timedelta

from csp_zeromq_adapter import ZeroMQAdapter


def test_pub_sub_str_message(graph_runner, timeout_realtime_engine_node):
    @csp.node
    def kill_engine(messages: csp.ts[str], n: int) -> csp.ts[bool]:
        with csp.state():
            received_messages: int = 0
        if csp.ticked(messages):
            received_messages += 1
            if received_messages >= n:
                return True

    @csp.graph
    def g(n: int):
        adapter_manager = ZeroMQAdapter()

        pub_socket = adapter_manager.pub(uri="inproc://test_pub_sub_str_message", bind=True)
        sub_socket = adapter_manager.sub(uri="inproc://test_pub_sub_str_message", connect=True)

        pub_socket.publish("", csp.curve(str, [(timedelta(0), f"Message {i}") for i in range(n)]))
        subscribed_messages = sub_socket.subscribe("", str)
        csp.add_graph_output("subscribed_messages", subscribed_messages)

        csp.stop_engine(
            csp.flatten([kill_engine(subscribed_messages, n), timeout_realtime_engine_node(timedelta(seconds=5))])
        )

    expected_num_messages = 5
    output = graph_runner(g, expected_num_messages)

    assert len(output["subscribed_messages"]) == expected_num_messages
    assert [payload[1] for payload in output["subscribed_messages"]] == [
        f"Message {i}" for i in range(expected_num_messages)
    ]


def test_pub_sub_struct_message(graph_runner, timeout_realtime_engine_node):
    class MyStruct(csp.Struct):
        message: str

    @csp.node
    def kill_engine(messages: csp.ts[MyStruct], n: int) -> csp.ts[bool]:
        with csp.state():
            received_messages: int = 0
        if csp.ticked(messages):
            received_messages += 1
            if received_messages >= n:
                return True

    @csp.graph
    def g(n: int):
        adapter_manager = ZeroMQAdapter()

        pub_socket = adapter_manager.pub(uri="inproc://test_pub_sub_struct_message", bind=True)
        sub_socket = adapter_manager.sub(uri="inproc://test_pub_sub_struct_message", connect=True)

        pub_socket.publish(
            "",
            csp.curve(MyStruct, [(timedelta(0), MyStruct(message=f"Message {i}")) for i in range(n)]),
            msg_mapper=JSONTextMessageMapper(),
        )
        subscribed_messages = sub_socket.subscribe("", MyStruct, msg_mapper=JSONTextMessageMapper())
        csp.add_graph_output("subscribed_messages", subscribed_messages)

        csp.stop_engine(
            csp.flatten([kill_engine(subscribed_messages, n), timeout_realtime_engine_node(timedelta(seconds=5))])
        )

    expected_num_messages = 5
    output = graph_runner(g, expected_num_messages)

    assert len(output["subscribed_messages"]) == expected_num_messages
    assert [payload[1] for payload in output["subscribed_messages"]] == [
        MyStruct(message=f"Message {i}") for i in range(expected_num_messages)
    ]


def test_pub_sub_str_message_multiple_topics(graph_runner, timeout_realtime_engine_node):
    @csp.node
    def kill_engine(messages: csp.ts[str], n: int) -> csp.ts[bool]:
        with csp.state():
            received_messages: int = 0
        if csp.ticked(messages):
            received_messages += 1
            if received_messages >= n:
                return True

    @csp.graph
    def g(n: int, m: int):
        adapter_manager = ZeroMQAdapter()

        pub_socket = adapter_manager.pub(uri="inproc://test_pub_sub_str_message_multiple_topics", bind=True)
        sub_socket = adapter_manager.sub(uri="inproc://test_pub_sub_str_message_multiple_topics", connect=True)

        all_subscriptions = []
        for topic_num in range(m):
            pub_socket.publish(
                f"topic{topic_num}",
                csp.curve(str, [(timedelta(0), f"Message {i} topic{topic_num}") for i in range(n)]),
            )
            subscribed_messages = sub_socket.subscribe(f"topic{topic_num}", str)
            all_subscriptions.append(subscribed_messages)
            csp.add_graph_output(f"subscribed_messages_topic_{topic_num}", subscribed_messages)

        csp.stop_engine(
            csp.flatten(
                [
                    kill_engine(csp.flatten(all_subscriptions), n * m),
                    timeout_realtime_engine_node(timedelta(seconds=10)),
                ]
            )
        )

    expected_num_messages = 10
    num_topics = 5
    output = graph_runner(g, expected_num_messages, num_topics)
    for topic_num in range(num_topics):
        assert len(output[f"subscribed_messages_topic_{topic_num}"]) == expected_num_messages
        assert [payload[1] for payload in output[f"subscribed_messages_topic_{topic_num}"]] == [
            f"Message {i} topic{topic_num}" for i in range(expected_num_messages)
        ]
