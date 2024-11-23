import csp
import pytest
from datetime import timedelta

from csp_zeromq_adapter import ZeroMQAdapter


def test_pull_raises_bind(graph_runner, timeout_realtime_engine_node):
    @csp.graph
    def g():
        adapter = ZeroMQAdapter()

        pull_socket = adapter.pull(uri="notsomethingicanbindto", ts_type=str, bind=True, connect=False)

        csp.stop_engine(timeout_realtime_engine_node())

    with pytest.raises(Exception) as excinfo:
        graph_runner(g)

        assert str(excinfo.value) == "RuntimeException: cannot bind to: notsomethingicanbindto"


def test_pull_raises_connect(graph_runner, timeout_realtime_engine_node):
    @csp.graph
    def g():
        adapter = ZeroMQAdapter()

        pull_socket = adapter.pull(uri="notsomethingicanconnectto")

        csp.stop_engine(timeout_realtime_engine_node())

    with pytest.raises(Exception) as excinfo:
        graph_runner(g)

        assert str(excinfo.value) == "RuntimeException: cannot connect to: notsomethingicanconnectto"
