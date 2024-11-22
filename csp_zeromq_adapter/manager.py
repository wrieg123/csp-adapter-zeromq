import csp
from csp import ts
from csp.adapters.utils import MsgMapper, RawTextMessageMapper
from csp.impl.types.container_type_normalizer import ContainerTypeNormalizer
from csp.impl.wiring import input_adapter_def, output_adapter_def
from datetime import timedelta
from typing import Any, Dict, Optional, TypeVar

from csp_zeromq_adapter.base_socket import BaseSocket
from csp_zeromq_adapter.lib import _cspzmqlibimpl

T = TypeVar("T")


class Manager:
    def __init__(self, io_threads: int):
        self._io_threads = io_threads

    def register_pub_socket(self, uri: str, bind: bool, connect: bool, timeout: timedelta) -> "PubSocket":
        return PubSocket(manager=self, uri=uri, bind=bind, connect=connect, timeout=timeout)

    def register_sub_socket(self, uri: str, bind: bool, connect: bool, timeout: timedelta) -> "SubSocket":
        return SubSocket(manager=self, uri=uri, bind=bind, connect=connect, timeout=timeout)

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
