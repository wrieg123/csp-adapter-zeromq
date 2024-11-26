import csp
import pytest
from csp import ts
from datetime import timedelta

from csp_adapter_zeromq import ZeroMQAdapter


def test_sub_raises_bind(graph_runner, timeout_realtime_engine_node):
    @csp.graph
    def g():
        adapter = ZeroMQAdapter()

        sub_socket = adapter.sub(uri="notsomethingicanbindtosub", bind=True, connect=False)

        sub_socket.subscribe("", str)

        csp.stop_engine(timeout_realtime_engine_node(timeout=timedelta(seconds=1)))

    with pytest.raises(Exception) as excinfo:
        graph_runner(g)

        assert str(excinfo.value) == "RuntimeException: cannot bind to: notsomethingicanbindtosub"


def test_sub_raises_connect(graph_runner, timeout_realtime_engine_node):
    @csp.graph
    def g():
        adapter = ZeroMQAdapter()

        sub_socket = adapter.sub(uri="notsomethingicanconnecttosub", bind=False, connect=True)

        sub_socket.subscribe("", str)

        csp.stop_engine(timeout_realtime_engine_node(timeout=timedelta(seconds=1)))

    with pytest.raises(Exception) as excinfo:
        graph_runner(g)

        assert str(excinfo.value) == "RuntimeException: cannot connect to: notsomethingicanconnecttosub"
