import csp
import pytest
from csp import ts
from datetime import timedelta

from csp_zeromq_adapter import ZeroMQAdapter


def test_pub_raises_bind(graph_runner, timeout_realtime_engine_node):
    @csp.graph
    def g():
        adapter = ZeroMQAdapter()

        pub_socket = adapter.pub(uri="notsomethingicanbindto")

        pub_socket.publish("", csp.curve(str, [(timedelta(0), "test")]))

        csp.stop_engine(timeout_realtime_engine_node)

    with pytest.raises(Exception) as excinfo:
        graph_runner(g)

        assert str(excinfo.value) == "RuntimeException: cannot bind to: notsomethingicanbindto"


def test_pub_raises_connect(graph_runner, timeout_realtime_engine_node):
    @csp.graph
    def g():
        adapter = ZeroMQAdapter()

        pub_socket = adapter.pub(uri="notsomethingicanconnectto", bind=False, connect=True)

        pub_socket.publish("", csp.curve(str, [(timedelta(0), "test")]))
        csp.stop_engine(timeout_realtime_engine_node)

    with pytest.raises(Exception) as excinfo:
        graph_runner(g)

        assert str(excinfo.value) == "RuntimeException: cannot connect to: notsomethingicanconnectto"
