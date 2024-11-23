import csp
from csp import ts
from csp.adapters.utils import JSONTextMessageMapper
from datetime import timedelta

from csp_zeromq_adapter import ZeroMQAdapter


def test_push_pull_str_message(graph_runner, timeout_realtime_engine_node):
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

        push_socket = adapter_manager.push(uri="inproc://test_push_pull_str_message", bind=True)
        pulled_messages = adapter_manager.pull(uri="inproc://test_push_pull_str_message", ts_type=str, connect=True)

        push_socket.push(csp.curve(str, [(timedelta(0), f"Message {i}") for i in range(n)]))
        csp.add_graph_output("pulled_messages", pulled_messages)

        csp.stop_engine(
            csp.flatten([kill_engine(pulled_messages, n), timeout_realtime_engine_node(timedelta(seconds=5))])
        )

    expected_num_messages = 5
    output = graph_runner(g, expected_num_messages)

    assert len(output["pulled_messages"]) == expected_num_messages
    assert [payload[1] for payload in output["pulled_messages"]] == [
        f"Message {i}" for i in range(expected_num_messages)
    ]


def test_push_pull_struct_message(graph_runner, timeout_realtime_engine_node):
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

        push_socket = adapter_manager.push(uri="inproc://test_push_pull_struct_message", bind=True)
        pulled_messages = adapter_manager.pull(
            uri="inproc://test_push_pull_struct_message",
            ts_type=MyStruct,
            msg_mapper=JSONTextMessageMapper(),
            connect=True,
        )

        push_socket.push(
            csp.curve(MyStruct, [(timedelta(0), MyStruct(message=f"Message {i}")) for i in range(n)]),
            msg_mapper=JSONTextMessageMapper(),
        )
        csp.add_graph_output("pulled_messages", pulled_messages)

        csp.stop_engine(
            csp.flatten([kill_engine(pulled_messages, n), timeout_realtime_engine_node(timedelta(seconds=5))])
        )

    expected_num_messages = 5
    output = graph_runner(g, expected_num_messages)

    assert len(output["pulled_messages"]) == expected_num_messages
    assert [payload[1] for payload in output["pulled_messages"]] == [
        MyStruct(message=f"Message {i}") for i in range(expected_num_messages)
    ]
