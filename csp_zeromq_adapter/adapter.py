import csp
from csp import ts
from csp.adapters.utils import MsgMapper, RawTextMessageMapper
from datetime import timedelta
from typing import Any, Dict, Optional, TypeVar

from csp_zeromq_adapter.manager import Manager, PubSocket, PushSocket, SubSocket

T = TypeVar("T")


class ZeroMQAdapter:
    """
    The ZeroMQAdapter creates a single context that is shared amonst all child sockets created from it.

    Args
    ----
    io_threads: int = 1
        Number of io_threads to use with the ZMQ context.
    """

    def __init__(self, io_threads: int = 1):
        assert io_threads >= 1, "Must have at least 1 context io thread."
        self._adapter_manager: Manager = Manager(io_threads=io_threads)

    def pub(
        self, uri: str, bind: bool = True, connect: bool = False, timeout: timedelta = timedelta(milliseconds=100)
    ) -> PubSocket:
        """
        Creates a `PUB` ZeroMQ socket. Messages are published via one background thread.

        Args
        ----
        uri: str
            resource to target
        bind: bool = True
            bind the zeromq socket to the `uri`
        connect: bool = False
            connect the zeromq socket to the `uri`
        timeout: timedelta = timedelta(milliseconds=100)
            how long to block the background thread when waiting for messages to send

        """
        return self._adapter_manager.register_pub_socket(
            uri=uri,
            bind=bind,
            connect=connect,
            timeout=timeout,
        )

    def sub(
        self, uri: str, connect: bool = True, bind: bool = False, timeout: timedelta = timedelta(milliseconds=100)
    ) -> SubSocket:
        """
        Creates a `SUB` ZeroMQ socket. When multiple subscriptions are made, the sockets are polled in a round-robin.

        Args
        ----
        uri: str
            resource to target
        bind: bool = True
            bind the zeromq socket to the `uri`
        connect: bool = False
            connect the zeromq socket to the `uri`
        timeout: timedelta = timedelta(milliseconds=100)
            how long to block the background thread when receiving messages
        """
        return self._adapter_manager.register_sub_socket(uri=uri, bind=bind, connect=connect, timeout=timeout)

    def push(
        self, uri: str, bind: bool = True, connect: bool = False, timeout: timedelta = timedelta(milliseconds=100)
    ) -> PushSocket:
        """
        Creates a `PUSH` ZeroMQ socket. Messages are published via one background thread.

        Args
        ----
        uri: str
            resource to target
        bind: bool = True
            bind the zeromq socket to the `uri`
        connect: bool = False
            connect the zeromq socket to the `uri`
        timeout: timedelta = timedelta(milliseconds=100)
            how long to block the background thread when waiting for messages to send

        """
        return self._adapter_manager.register_push_socket(
            uri=uri,
            bind=bind,
            connect=connect,
            timeout=timeout,
        )

    def pull(
        self,
        uri: str,
        ts_type: type,
        bind: bool = False,
        connect: bool = True,
        timeout: timedelta = timedelta(milliseconds=100),
        msg_mapper: MsgMapper = RawTextMessageMapper(),
        field_map: Optional[Dict[str, Any] | str] = None,
        meta_field_map: Optional[Dict[str, Any]] = None,
        push_mode: csp.PushMode = csp.PushMode.NON_COLLAPSING,
    ) -> ts["T"]:
        """
        Creates a `PULL` ZeroMQ socket. The return type is a ticking time series of messages from the socket.

        Args
        ----
        uri: str
            resource to target
        ts_type: type
            `csp.ts` type that the edge will return
        bind: bool = True
            bind the zeromq socket to the `uri`
        connect: bool = False
            connect the zeromq socket to the `uri`
        timeout: timedelta = timedelta(milliseconds=100)
            how long to block the background thread when waiting for messages to send

        Kwargs
        ------
        msg_mapper: MsgMapper = RawTextMessageMapper()
            message mapper to use when converting the ticking edge to `ts_type`
        field_map: Optional[Dict[str, Any]] = None
            mapping of fields to struct field attributes
        meta_field_map: Optional[Dict[str, Any]] = None
            meta information used in the struct converter, check the CSP docs
        push_mode: csp.PushMode = csp.PushMode.NON_COLLAPSING
            push mode and batching used on the InputAdapter
        """
        return self._adapter_manager.register_pull_socket(
            uri=uri,
            bind=bind,
            connect=connect,
            timeout=timeout,
        ).pull(
            ts_type=ts_type,
            msg_mapper=msg_mapper,
            field_map=field_map,
            meta_field_map=meta_field_map,
            push_mode=push_mode,
        )

    def _create(self, engine, memo):
        return self._adapter_manager._create(engine=engine, memo=memo)
