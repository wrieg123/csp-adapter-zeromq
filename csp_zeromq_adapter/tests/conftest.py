import csp
import pytest
import pytz
from csp import ts
from datetime import datetime, timedelta


@pytest.fixture
def timeout_realtime_engine_node():
    @csp.node
    def _timeout_node(timeout: timedelta = timedelta(seconds=10)) -> csp.ts[bool]:
        with csp.alarms():
            a_timeout: ts[bool] = csp.alarm(bool)

        with csp.start():
            csp.schedule_alarm(a_timeout, timeout, True)

        if csp.ticked(a_timeout):
            print("Stoping test due to timeout after ", timeout)
            return True

    return _timeout_node


@pytest.fixture
def graph_runner():
    def _runner(
        g,
        *args,
        starttime: datetime = datetime.now(pytz.UTC),
        endtime: datetime = timedelta(seconds=10),
        realtime: bool = True,
    ):
        return csp.run(g, *args, starttime=starttime, endtime=endtime, realtime=realtime)

    return _runner
