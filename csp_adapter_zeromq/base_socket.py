import csp
from csp.adapters.utils import MsgMapper
from datetime import timedelta
from typing import Any, Dict, Optional, TypeVar

Manager = TypeVar("Manager")


class BaseSocket:
    def __init__(
        self, manager: "Manager", uri: str, bind: bool, connect: bool, timeout: timedelta = timedelta(milliseconds=100)
    ):
        self._manager = manager
        self._uri = uri
        self._bind = bind
        self._connect = connect
        self._timeout = timeout

    def _create_properties_from_msg_mapper(
        self,
        ts_type: type,
        msg_mapper: MsgMapper,
        field_map: Optional[Dict[str, Any] | str],
        meta_field_map: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        field_map = field_map or {}
        meta_field_map = meta_field_map or {}
        if isinstance(field_map, str):
            field_map = {field_map: ""}

        if not field_map and issubclass(ts_type, csp.Struct):
            field_map = ts_type.default_field_map()

        properties = msg_mapper.properties.copy()
        properties["field_map"] = field_map
        properties["meta_field_map"] = meta_field_map
        return properties

    def _connection_details(self) -> Dict[str, Any]:
        return dict(
            uri=self._uri,
            bind=self._bind,
            connect=self._connect,
            timeout=self._timeout,
        )

    def _create_properties(
        self,
        ts_type: type,
        msg_mapper: MsgMapper,
        field_map: Optional[Dict[str, Any] | str],
        meta_field_map: Optional[Dict[str, Any]],
    ) -> Dict[str, Dict[str, Any]]:
        return dict(
            msg_mapper=self._create_properties_from_msg_mapper(
                ts_type=ts_type, msg_mapper=msg_mapper, field_map=field_map, meta_field_map=meta_field_map
            ),
            connection_details=self._connection_details(),
        )
