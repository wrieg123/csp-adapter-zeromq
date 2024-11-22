from datetime import timedelta

from csp_zeromq_adapter.manager import Manager, PubSocket, SubSocket


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

    def _create(self, engine, memo):
        return self._adapter_manager._create(engine=engine, memo=memo)
