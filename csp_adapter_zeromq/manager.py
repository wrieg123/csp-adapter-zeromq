import csp
from csp import ts
from csp.adapters.utils import MsgMapper, RawTextMessageMapper
from csp.impl.types.container_type_normalizer import ContainerTypeNormalizer
from csp.impl.wiring import input_adapter_def, output_adapter_def
from datetime import timedelta
from typing import Any, Dict, Optional, TypeVar

from csp_adapter_zeromq.base_socket import BaseSocket
from csp_adapter_zeromq.lib import _cspzmqlibimpl

T = TypeVar("T")


class Manager:
    def __init__(self, io_threads: int):
        self._io_threads = io_threads

    def register_pub_socket(self, uri: str, bind: bool, connect: bool, timeout: timedelta) -> "PubSocket":
        return PubSocket(manager=self, uri=uri, bind=bind, connect=connect, timeout=timeout)

    def register_sub_socket(self, uri: str, bind: bool, connect: bool, timeout: timedelta) -> "SubSocket":
        return SubSocket(manager=self, uri=uri, bind=bind, connect=connect, timeout=timeout)

    def register_push_socket(self, uri: str, bind: bool, connect: bool, timeout: timedelta) -> "PushSocket":
        return PushSocket(manager=self, uri=uri, bind=bind, connect=connect, timeout=timeout)

    def register_pull_socket(self, uri: str, bind: bool, connect: bool, timeout: timedelta) -> "PullSocket":
        return PullSocket(manager=self, uri=uri, bind=bind, connect=connect, timeout=timeout)

    def _get_properties(self) -> Dict[str, Any]:
        return dict(io_threads=self._io_threads)

    def _create(self, engine, memo):
        return _cspzmqlibimpl._adapter_manager(engine, self._get_properties())


class PubSocket(BaseSocket):
    def publish(
        self,
        topic: str,
        edge: ts["T"],
        msg_mapper: MsgMapper = RawTextMessageMapper(),
        field_map: Optional[Dict[str, Any] | str] = None,
        meta_field_map: Optional[Dict[str, Any]] = None,
    ):
        """
        Publish a ticking edge over the topic.

        Args
        ----
        topic: str
            topic to publish the ticking edge to
        edge: ts['T']
            ticking edge with messages to publish

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
        properties = self._create_properties(
            ts_type=edge.tstype.typ, msg_mapper=msg_mapper, field_map=field_map, meta_field_map=meta_field_map
        )
        properties["topic"] = topic
        ts_type = ContainerTypeNormalizer.normalized_type_to_actual_python_type(edge.tstype.typ)
        return _pub_socket_output_adapter_def(self._manager, edge, ts_type, properties)


_pub_socket_output_adapter_def = output_adapter_def(
    "pub_socket_output_adapter",
    _cspzmqlibimpl._pub_socket_output_adapter,
    Manager,
    input=ts["T"],
    typ="T",
    properties=dict,
)


class SubSocket(BaseSocket):
    def subscribe(
        self,
        topic: str,
        ts_type: type,
        msg_mapper: MsgMapper = RawTextMessageMapper(),
        field_map: Optional[Dict[str, Any] | str] = None,
        meta_field_map: Optional[Dict[str, Any]] = None,
        push_mode: csp.PushMode = csp.PushMode.NON_COLLAPSING,
    ):
        """
        Subscribe to a given topic and convert messages.

        Args
        ----
        topic: str
            topic to receive messages from
        ts_type: type
            expected input type on the ticking edge

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
        properties = self._create_properties(
            ts_type=ts_type, msg_mapper=msg_mapper, field_map=field_map, meta_field_map=meta_field_map
        )
        properties["topic"] = topic
        return _sub_socket_input_adapter_def(self._manager, ts_type, properties, push_mode=push_mode)


_sub_socket_input_adapter_def = input_adapter_def(
    "sub_socket_input_adapter",
    _cspzmqlibimpl._sub_socket_input_adapter,
    ts["T"],
    Manager,
    typ="T",
    properties=dict,
)


class PushSocket(BaseSocket):
    def push(
        self,
        edge: ts["T"],
        msg_mapper: MsgMapper = RawTextMessageMapper(),
        field_map: Optional[Dict[str, Any] | str] = None,
        meta_field_map: Optional[Dict[str, Any]] = None,
    ):
        """
        Push a ticking edge onto the socket.

        Args
        ----
        edge: ts['T']
            ticking edge with messages to push

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
        properties = self._create_properties(
            ts_type=edge.tstype.typ, msg_mapper=msg_mapper, field_map=field_map, meta_field_map=meta_field_map
        )
        ts_type = ContainerTypeNormalizer.normalized_type_to_actual_python_type(edge.tstype.typ)
        return _push_socket_output_adapter_def(self._manager, edge, ts_type, properties)


_push_socket_output_adapter_def = output_adapter_def(
    "push_socket_output_adapter",
    _cspzmqlibimpl._push_socket_output_adapter,
    Manager,
    input=ts["T"],
    typ="T",
    properties=dict,
)


class PullSocket(BaseSocket):
    def pull(
        self,
        ts_type: type,
        msg_mapper: MsgMapper = RawTextMessageMapper(),
        field_map: Optional[Dict[str, Any] | str] = None,
        meta_field_map: Optional[Dict[str, Any]] = None,
        push_mode: csp.PushMode = csp.PushMode.NON_COLLAPSING,
    ):
        """
        Pull messages from the socket.

        Args
        ----
        ts_type: type
            expected input type on the ticking edge

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
        properties = self._create_properties(
            ts_type=ts_type, msg_mapper=msg_mapper, field_map=field_map, meta_field_map=meta_field_map
        )
        return _pull_socket_input_adapter_def(self._manager, ts_type, properties, push_mode=push_mode)


_pull_socket_input_adapter_def = input_adapter_def(
    "pull_socket_input_adapter",
    _cspzmqlibimpl._pull_socket_input_adapter,
    ts["T"],
    Manager,
    typ="T",
    properties=dict,
)
