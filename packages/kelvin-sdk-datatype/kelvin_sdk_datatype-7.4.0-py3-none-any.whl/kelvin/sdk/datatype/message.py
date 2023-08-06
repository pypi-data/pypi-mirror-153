"""Data-Model Messages."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from copy import deepcopy
from datetime import datetime, timezone
from enum import Enum
from functools import wraps
from importlib import import_module
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    List,
    Mapping,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

from cloudevents.sdk.event.v1 import Event
from pydantic import BaseModel, Extra, Field, validator
from pydantic.fields import SHAPE_LIST, SHAPE_MAPPING, SHAPE_SINGLETON, ModelField
from pydantic.schema import default_ref_template
from pydantic.types import ConstrainedFloat, ConstrainedInt, ConstrainedStr
from pydantic.typing import display_as_type

from .model import CoreHeader, CoreModel, CoreModelMeta, Model
from .utils import format_code, from_rfc3339_timestamp, gather, to_rfc3339_timestamp

# legacy type names
from .types import (  # isort:skip
    Float32_,
    Float64_,
    Int8_,
    Int16_,
    Int32_,
    Int64_,
    UInt8_,
    UInt16_,
    UInt32_,
    UInt64_,
)

CONSTRAINT_NAMES = [
    "gt",
    "lt",
    "ge",
    "le",
    "min_length",
    "max_length",
    "min_items",
    "max_items",
]

FLAT_KEYS = {"data_type", "payload", "timestamp"}


def format_annotation(x: ModelField, imports: Mapping[str, Set[str]]) -> str:
    """Format annotation."""

    kwargs: Dict[str, Any] = {}

    if x.default_factory is not None:
        kwargs["default_factory"] = x.default_factory
    elif x.default is not None:
        kwargs["default"] = x.default
    else:
        kwargs["default"] = ... if x.required else None

    if x.field_info.description:
        kwargs["description"] = x.field_info.description

    if issubclass(x.type_, Enum):
        annotation = x.type_.__name__
    elif (
        issubclass(x.type_, (ConstrainedFloat, ConstrainedInt, ConstrainedStr))
        and x.type_.__module__ != "kelvin.sdk.datatype.types"
    ):
        kwargs.update(
            {
                k: v
                for k, v in ((name, getattr(x.type_, name, None)) for name in CONSTRAINT_NAMES)
                if v is not None
            }
        )
        annotation = display_as_type(x.type_.mro()[-2])
    else:
        annotation = display_as_type(x.type_)

    if x.shape == SHAPE_LIST:
        annotation = f"List[{annotation}]"
    elif x.shape == SHAPE_MAPPING:
        annotation = f"Dict[str, {annotation}]"

    if x.allow_none:
        annotation = f"Optional[{annotation}]"

    def repr_val(x: Any) -> str:
        if x is ...:
            return "..."
        if callable(x):
            return x.__name__
        return repr(x)

    field_args: List[str] = []
    if "default" in kwargs:
        field_args += [repr_val(kwargs.pop("default"))]
    field_args += (f"{k}={repr_val(v)}" for k, v in kwargs.items())

    result = f"{annotation} = Field({', '.join(field_args)})"

    # substitute imports
    for module, names in imports.items():
        for name in names:
            result = re.sub(rf"\b{module}.{name}\b", name, result)

    return result


class Endpoint(Model):
    """Message endpoint."""

    node_name: Optional[str] = Field(None, title="Node Name", description="Node name.")
    workload_name: Optional[str] = Field(None, title="Workload Name", description="Workload name.")

    def __str__(self) -> str:
        """String representation."""

        if not self.node_name and not self.workload_name:
            return ""
        return f"{self.node_name or ''}/{self.workload_name or ''}"


class Header(CoreHeader):
    """Header Interface."""

    @validator("name", pre=True, always=True)
    def validate_name(cls, value: Any) -> str:
        """Validate name."""

        return value if value is not None else ""

    @validator("source", "target", pre=True, always=True)
    def validate_endpoints(cls, value: Any) -> Any:
        """Validate endpoints."""

        if not value:
            return None

        if not isinstance(value, str):
            return value

        if value.count("/") != 1:
            raise ValueError("Invalid topic") from None

        node_name, workload_name = value.split("/", 1)

        return {"node_name": node_name, "workload_name": workload_name}

    type: str = Field(..., title="Message Type", description="Message type.")
    name: str = Field(..., title="Message Name", description="Message name.")
    id: Optional[str] = Field(None, title="ID", description="Unique message ID.")
    trace_id: Optional[str] = Field(None, title="Trace ID", description="Message Trace ID.")
    source: Endpoint = Field(None, title="Message Source", description="Message source.")
    target: Endpoint = Field(None, title="Message Target", description="Message target.")
    asset_name: Optional[str] = Field(None, title="Asset Name", description="Asset name.")

    @wraps(BaseModel.dict)
    def dict(
        self,
        by_alias: bool = True,
        exclude_none: bool = True,
        exclude_unset: bool = False,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Generate a dictionary representation of the model."""

        result = super().dict(
            by_alias=by_alias, exclude_none=exclude_none, exclude_unset=exclude_unset, **kwargs
        )

        if self.source:
            result["source"] = str(self.source)
        if self.target:
            result["target"] = str(self.target)

        return result


class MessageMeta(CoreModelMeta):
    """Message metaclass."""

    MESSAGE_TYPES: Dict[str, Type[Message]] = {}

    def __new__(
        metacls: Type[MessageMeta], name: str, bases: Tuple[Type, ...], __dict__: Dict[str, Any]
    ) -> MessageMeta:
        """Create Message class."""

        if "Config" not in __dict__ and all(
            x.startswith("_") for x in __dict__.get("__annotations__", {})
        ):

            class Config:
                extra = Extra.allow

            Config.__qualname__ = f"{name}.Config"

            __dict__["Config"] = Config

        cls = cast(MessageMeta, super().__new__(metacls, name, bases, __dict__))

        _type = __dict__.get("_TYPE")

        if isinstance(_type, str):
            metacls.MESSAGE_TYPES[_type] = cast(Type[Message], cls)

        return cls


T = TypeVar("T", bound="Message")


class Message(CoreModel[Header], metaclass=MessageMeta):
    """Message Interface."""

    _TYPE: str

    _SPEC_VERSION: int = 1

    _DOMAIN: str = "data"

    __slots__ = ("_TYPE",)

    class Config(CoreModel.Config):
        """Pydantic config."""

        @staticmethod
        def schema_extra(schema: Dict[str, Any], model_class: Type[CoreModel]) -> None:  # type: ignore
            """Make schema additions."""

            definitions = schema.setdefault("definitions", {})
            properties = schema.get("properties", {})

            for name, field in model_class.__fields__.items():
                T = field.type_
                if (
                    not issubclass(T, (ConstrainedFloat, ConstrainedInt))
                    or T.__module__ != "kelvin.sdk.datatype.types"
                ):
                    continue

                type_name = T.__name__[:-1]

                field_schema = properties[name]
                if field.shape == SHAPE_LIST:
                    field_schema = field_schema["items"]
                field_schema.pop("type")
                field_schema.pop("minimum", None)
                field_schema.pop("maximum", None)
                field_schema["$ref"] = default_ref_template.format(model=type_name)

                if type_name in definitions:
                    continue

                definitions[type_name] = {
                    "title": type_name,
                    "description": T.__doc__,
                    "type": "integer" if issubclass(T, int) else "number",
                    "minimum": T.ge,
                    "maximum": T.le,
                }

    def __new__(cls, *args: Any, **kwargs: Any) -> Message:
        """Initialise message."""

        if isinstance(cls._TYPE, str):
            T = cls
        else:
            try:
                _type = kwargs["_"]["type"]
            except KeyError:
                try:
                    _type = kwargs["data_type"]
                except KeyError:
                    raise ValueError("Missing message type") from None

            T = cls.get_type(_type)

        obj = super().__new__(T)

        # only init if args provided
        if args or kwargs:
            obj.__init__(*args, **kwargs)

        return obj

    def __init__(
        self,
        _name: Optional[str] = None,
        *,
        _: Optional[Union[Header, Mapping[str, Any]]] = None,
        **kwargs: Any,
    ) -> None:
        """Initialise message."""

        _type: str = self._TYPE

        if _ is not None:
            if isinstance(_, Header):
                pass
            elif isinstance(_, Mapping):
                _ = Header.parse_obj({"type": _type, "name": _name, **_})
            else:
                raise ValueError(f"Invalid header type: {type(_).__name__!r}") from None

            _ = cast(Header, _)
            if _.type != _type:
                raise ValueError(f"Header type mismatch {_.type!r} != {_type!r}") from None
            if _name is not None and _.name != _name:
                raise ValueError(f"Header name mismatch {_.name!r} != {_name!r}") from None
        elif kwargs.keys() >= FLAT_KEYS:
            # reinflate header
            timestamp = from_rfc3339_timestamp(kwargs.pop("timestamp"))
            data_type = kwargs.pop("data_type")
            payload = kwargs.pop("payload")
            _ = kwargs
            _["time_of_validity"] = int(timestamp.timestamp() * 1e9)
            _["type"] = data_type
            kwargs = payload
        else:
            _ = Header(name=_name, type=_type)

        super().__init__(_, **kwargs)

    @classmethod
    def to_code(cls) -> str:
        """Generate code."""

        result: List[str] = [f'"""{cls.__name__} Message."""', ""]
        extra: List[str] = []

        imports: Dict[str, Set[str]] = defaultdict(set)
        imports["__future__"] |= {"annotations"}
        imports["typing"] |= {*[]}
        imports["pydantic"] |= {"Field"}
        if not cls.__fields__:
            imports["pydantic"] |= {"Extra"}
        imports["kelvin.sdk.datatype.message"] |= {"Message"}

        for name, field in cls.__fields__.items():
            if field.shape == SHAPE_LIST:
                imports["typing"] |= {"List"}
            elif field.shape == SHAPE_MAPPING:
                imports["typing"] |= {"Dict"}
            elif field.shape != SHAPE_SINGLETON:
                raise TypeError(f"Field {name!r} has invalid shape: {field.shape}") from None
            if field.allow_none:
                imports["typing"] |= {"Optional"}

            if (
                issubclass(field.type_, Message)
                or field.type_.__module__ == "kelvin.sdk.datatype.types"
            ):
                imports[field.type_.__module__] |= {field.type_.__name__}
            elif issubclass(field.type_, Enum):
                enum_base = field.type_.mro()[1]
                imports[enum_base.__module__] |= {enum_base.__name__}
                extra += [
                    f"class {field.type_.__name__}({enum_base.__name__}):",
                    f'    """{field.type_.__name__} enumeration."""',
                    *(f"    {x.name} = {x.value!r}" for x in field.type_),
                ]

        result += [f"from {k} import {', '.join(sorted(v))}" for k, v in imports.items() if k and v]
        result += [f"import {x}" for k, v in imports.items() if not k for x in sorted(v)]

        result += [
            *extra,
            f'''
class {cls.__name__}(Message):
    """{cls.__doc__ if cls.__doc__ else f"{cls.__name__} Message."}"""

    _TYPE = "{cls._TYPE}"
''',
        ]

        if not cls.__fields__:
            result += [
                "    class Config:",
                "        extra = Extra.allow",
            ]
        else:
            result += [
                f"    {name}: {format_annotation(field, imports)}"
                for name, field in cls.__fields__.items()
            ]

        return format_code("\n".join(result))

    @classmethod
    def get_type(cls, _type: str) -> Type[Message]:
        """Get message type by name."""

        try:
            return cls.MESSAGE_TYPES[_type]
        except KeyError:
            try:
                import_module(f"kelvin.message.{_type}")
            except ImportError:
                raise ValueError(f"Unknown message type: {_type}") from None
            try:
                return cls.MESSAGE_TYPES[_type]
            except KeyError:  # pragma: no cover
                raise ValueError(f"Unknown message type: {_type}") from None

    @classmethod
    def make_message(
        cls: Type[T],
        _type: str,
        _name: Optional[str] = None,
        _time_of_validity: Optional[Union[int, float]] = None,
        _source: Optional[Union[Endpoint, Mapping[str, Optional[str]]]] = None,
        _target: Optional[Union[Endpoint, Mapping[str, Optional[str]]]] = None,
        _asset_name: Optional[str] = None,
        _id: Optional[str] = None,
        _trace_id: Optional[str] = None,
        **kwargs: Any,
    ) -> T:
        """
        Create a message object.

        Parameters
        ----------
        _type : str, optional
            Message type (e.g. ``float32``, ``kelvin.beam_pump``)
        _name : str, optional
            Message name
        _time_of_validity : int, optional
            Time of validity in nano-seconds
        _source : dict, optional
            Message source
        _target : dict, optional
            Message target
        _asset_name : str, optional
            Asset name
        **kwargs :
            Additional properties for message (e.g. ``value`` for raw types)

        """

        _ = {
            "type": _type,
            "name": _name or None,
            "time_of_validity": _time_of_validity,
            "source": _source or None,
            "target": _target or None,
            "asset_name": _asset_name or None,
            "id": _id or None,
            "trace_id": _trace_id or None,
        }

        return cls(_=_, **kwargs)

    @wraps(BaseModel.schema)
    @classmethod
    def schema(
        cls, by_alias: bool = True, ref_template: str = default_ref_template
    ) -> Dict[str, Any]:
        """Generate schema dictionary."""

        result = deepcopy(super().schema(by_alias=by_alias, ref_template=ref_template))
        result["definitions"] = gather(result, "definitions")

        return result

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[..., Any], None, None]:
        """Get validators."""

        # preserve overridden class-method from pydantic
        yield super().validate

    def validate(self) -> bool:  # type: ignore
        """Check the validity of the message."""

        fields_set = self.__fields_set__

        return all(
            name in fields_set for name, field in self.__fields__.items() if not field.allow_none
        )

    @classmethod
    def from_event(cls: Type[T], event: Event) -> T:
        """Load from Cloud Event."""

        data: Dict[str, Any] = json.loads(event.data)

        if not isinstance(data, dict):
            raise ValueError(f"Event data of type {type(data).__name__!r} is not valid") from None

        header: Dict[str, Any] = data.setdefault("_", {})

        if "type" not in header:
            header["type"] = "object"

        if "name" not in header:
            event_source = event.source
            if event_source is not None:
                if event_source.startswith("/"):
                    event_source = event_source[1:].replace("/", ".")
                header["name"] = event_source

        if "time_of_validity" not in header:
            event_time = event.time
            if event_time is not None:
                timestamp = from_rfc3339_timestamp(event_time).timestamp()
                header["time_of_validity"] = int(timestamp * 1e9)

        return cls.parse_obj(data)

    def _lower(self, header: bool = True) -> Dict[str, Any]:
        """Convert to standard Python types."""

        result = dict(self._iter(by_alias=True, exclude_none=True, exclude_unset=True))
        result["_"] = self._.dict(exclude_none=True)

        if self._SPEC_VERSION == 2:
            result_ = result
            result = result_.pop("_")
            asset_name = result.pop("asset_name")
            metric_name = result.pop("name")
            result["resource"] = f"krn:am:{asset_name}/{metric_name}"
            data_type = result.pop("type")
            result["type"] = f"{self._DOMAIN};icd={data_type}"
            time_of_validity = result.pop("time_of_validity") / 1e9
            result["timestamp"] = to_rfc3339_timestamp(
                datetime.fromtimestamp(time_of_validity, timezone.utc)
            )
            result.pop("target", None)
            source = result.pop("source", None)
            if source:
                result["source"] = f"krn:wl:{source}"
            result["payload"] = result_

            return self._convert(result, header)

        if not header:
            result_ = result
            result = result_.pop("_")
            result["data_type"] = result.pop("type")
            time_of_validity = result.pop("time_of_validity") / 1e9
            result["timestamp"] = to_rfc3339_timestamp(
                datetime.fromtimestamp(time_of_validity, timezone.utc)
            )
            result["payload"] = result_

        return self._convert(result, header)

    # legacy interface
    def to_json(self) -> str:
        """Convert to JSON."""

        return json.dumps(self.dict(exclude_unset=True))

    @classmethod
    def from_json(cls: Type[T], x: str) -> T:
        """Load from JSON."""

        return cls.parse_raw(x)

    def clone(self: T) -> T:
        """Clone message."""

        return self.copy(deep=True)


class Object(Message):
    """Simple data-model."""

    _TYPE = "object"


class RawMessage(Message):
    """Message with a single value field."""

    value: Any


class Generic(RawMessage):
    _TYPE = "raw.generic"

    value: Any = Field(None, description="An arbitrary value")


class Boolean(RawMessage):
    """A raw boolean."""

    _TYPE = "raw.boolean"

    value: bool = Field(False, description="The raw boolean value.")


class Text(RawMessage):
    """A raw string."""

    _TYPE = "raw.text"

    value: str = Field("", description="The raw string value.")


class Float32(RawMessage):
    """A raw 32-bit floating point."""

    _TYPE = "raw.float32"

    value: Float32_ = Field(0.0, description="The raw 32-bit floating point value.")


class Float64(RawMessage):
    """A raw 64-bit floating point."""

    _TYPE = "raw.float64"

    value: Float64_ = Field(0.0, description="The raw 64-bit floating point value.")


class Int8(RawMessage):
    """A raw signed 8-bit integer."""

    _TYPE = "raw.int8"

    value: Int8_ = Field(0, description="The raw signed 8-bit integer value.")


class Int16(RawMessage):
    """A raw signed 16-bit integer."""

    _TYPE = "raw.int16"

    value: Int16_ = Field(0, description="The raw signed 16-bit integer value.")


class Int32(RawMessage):
    """A raw signed 32-bit integer."""

    _TYPE = "raw.int32"

    value: Int32_ = Field(0, description="The raw signed 32-bit integer value.")


class Int64(RawMessage):
    """A raw signed 64-bit integer."""

    _TYPE = "raw.int64"

    value: Int64_ = Field(0, description="The raw signed 64-bit integer value.")


class UInt8(RawMessage):
    """A raw unsigned 8-bit integer."""

    _TYPE = "raw.uint8"

    value: UInt8_ = Field(0, description="The raw unsigned 8-bit integer value.")


class UInt16(RawMessage):
    """A raw unsigned 16-bit integer."""

    _TYPE = "raw.uint16"

    value: UInt16_ = Field(0, description="The raw unsigned 16-bit integer value.")


class UInt32(RawMessage):
    """A raw unsigned 32-bit integer."""

    _TYPE = "raw.uint32"

    value: UInt32_ = Field(0, description="The raw unsigned 32-bit integer value.")


class UInt64(RawMessage):
    """A raw unsigned 64-bit integer."""

    _TYPE = "raw.uint64"

    value: UInt64_ = Field(0, description="The raw unsigned 64-bit integer value.")


class ControlChange(Message):
    """Generic Control Change Message"""

    _SPEC_VERSION = 2
    _TYPE = "kelvin.control_change"
    _DOMAIN = "control"

    timeout: Optional[int] = Field(description="Timeout for retries")
    retries: Optional[int] = Field(description="Max retries")
    expiration_date: str = Field(decription="")
    payload: Dict[str, Any] = Field(None, description="Control Change payload")


class StateEnum(str, Enum):
    ready = "ready"
    sent = "sent"
    failed = "failed"
    processed = "processed"
    applied = "applied"


class ControlChangeStatus(Message):
    """Generic Control Change Message"""

    _SPEC_VERSION = 2
    _TYPE = "kelvin.control_change_status"
    _DOMAIN = "control-status"

    state: StateEnum
    message: Optional[str] = Field(decription="")


class SensorData(Message):
    """Sensor data."""

    _TYPE = "kelvin.sensor_data"

    data: List[Float64_] = Field(..., description="Array of sensor measurements.", min_items=1)
    sample_rate: float = Field(..., description="Sensor sample-rate in Hertz.", gt=0.0)


make_message = Message.make_message
