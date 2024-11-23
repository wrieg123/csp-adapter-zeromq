import csp
import pytest
from datetime import timedelta

from csp_zeromq_adapter import ZeroMQAdapter


def test_push_raises_bind(graph_runner, timeout_realtime_engine_node):
    @csp.graph
    def g():
        adapter = ZeroMQAdapter()

        push_socket = adapter.push(uri="notsomethingicanbindto")

        push_socket.push(csp.curve(str, [(timedelta(0), "test")]))

        csp.stop_engine(timeout_realtime_engine_node())

    with pytest.raises(Exception) as excinfo:
        graph_runner(g)

        assert str(excinfo.value) == "RuntimeException: cannot bind to: notsomethingicanbindto"


def test_push_raises_connect(graph_runner, timeout_realtime_engine_node):
    @csp.graph
    def g():
        adapter = ZeroMQAdapter()

        push_socket = adapter.push(uri="notsomethingicanconnectto", bind=False, connect=True)

        push_socket.push(csp.curve(str, [(timedelta(0), "test")]))
        csp.stop_engine(timeout_realtime_engine_node())

    with pytest.raises(Exception) as excinfo:
        graph_runner(g)

        assert str(excinfo.value) == "RuntimeException: cannot connect to: notsomethingicanconnectto"
