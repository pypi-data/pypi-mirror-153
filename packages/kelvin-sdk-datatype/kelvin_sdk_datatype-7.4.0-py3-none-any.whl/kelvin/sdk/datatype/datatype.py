"""Interface Document."""

from __future__ import annotations

import re
from collections import Counter, defaultdict, deque
from enum import Enum, IntEnum, auto
from functools import wraps
from operator import attrgetter
from pathlib import Path
from textwrap import indent
from typing import Any
from typing import Counter as Counter_
from typing import (
    DefaultDict,
    Deque,
    Dict,
    List,
    Mapping,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    Union,
    cast,
)

from pydantic import BaseModel, Field, ValidationError, create_model, validator
from pydantic.fields import FieldInfo
from pydantic.main import ErrorWrapper
from pydantic.types import ConstrainedFloat, ConstrainedInt

from .exception import DataTypeError
from .message import Message
from .model import Model
from .types import (
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
from .utils import camel_name, flatten, is_identifier


class MissingTypeError(DataTypeError):
    """Missing type error."""


class UnresolvableError(DataTypeError):
    """Unresolvable type error."""


class FileType(Enum):
    """DataType File Type."""

    YAML = auto()
    PROTO = auto()


FILE_TYPES = {
    ".yml": FileType.YAML,
    ".yaml": FileType.YAML,
    ".proto": FileType.PROTO,
}

FIELD_INFO: Mapping[str, Tuple[Type, Mapping[str, Any]]] = {
    "string": (str, {"default": ""}),
    "boolean": (bool, {"default": False}),
    "int8": (Int8_, {"default": 0}),
    "int16": (Int16_, {"default": 0}),
    "int32": (Int32_, {"default": 0}),
    "int64": (Int64_, {"default": 0}),
    "uint8": (UInt8_, {"default": 0}),
    "uint16": (UInt16_, {"default": 0}),
    "uint32": (UInt32_, {"default": 0}),
    "uint64": (UInt64_, {"default": 0}),
    "float32": (Float32_, {"default": 0.0}),
    "float64": (Float64_, {"default": 0.0}),
    # deprecated
    "bool": (bool, {"default": False}),
    "float": (Float32_, {"default": 0.0}),
    "double": (Float64_, {"default": 0.0}),
}


class DataTypeBase(Model):
    """DataType base model."""

    class Config(Model.Config):
        """Pydantic config."""

    @wraps(BaseModel.dict)
    def dict(
        self,
        by_alias: bool = True,
        exclude_none: bool = True,
        exclude_unset: bool = True,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Generate a dictionary representation of the model."""

        return super().dict(
            by_alias=by_alias, exclude_none=exclude_none, exclude_unset=exclude_unset, **kwargs
        )


class MessageField(DataTypeBase):
    """Message field."""

    name: str
    type: str
    title: Optional[str] = None
    description: Optional[str] = None
    units: Optional[str] = None
    required: bool = True
    mapping: bool = False
    array: bool = False
    enum: Optional[Sequence[Mapping[str, Any]]] = None
    min: Optional[Union[int, float]] = None
    max: Optional[Union[int, float]] = None

    @validator("enum", pre=True, always=True)
    def validate_enum(cls, value: Any) -> Any:
        """Validate enum field."""

        if not isinstance(value, Sequence):
            return value

        if not value:
            raise ValueError("enum must have at least one item")

        errors: List[ErrorWrapper] = []
        for i, x in enumerate(value):
            if not isinstance(x, Mapping):
                errors += [ErrorWrapper(ValueError(f"Level must be a mapping: {x!r}"), loc=(i,))]
            elif not all(isinstance(key, str) for key in x):
                errors += [ErrorWrapper(ValueError(f"Level names be strings: {x!r}"), loc=(i,))]

        if errors:
            raise ValidationError(errors, model=cast(Type[BaseModel], cls))

        return value

    def get_field_info(
        self, models: Optional[Mapping[str, Type[Message]]] = None
    ) -> Tuple[Any, FieldInfo]:
        """Get Pydantic field info."""

        if self.type in FIELD_INFO:
            type_, kwargs = FIELD_INFO[self.type]
            if self.enum:
                T: Type[Enum]
                if issubclass(type_, int):
                    T = IntEnum
                else:
                    T = Enum
                levels = {k: type_(v) for x in self.enum for k, v in x.items()}
                type_ = cast(Type[Enum], T(camel_name(self.name), levels))  # type: ignore
                kwargs = {"default": ...}
            else:
                kwargs = {**kwargs}
        elif models is not None and self.type in models:
            type_ = models[self.type]
            kwargs = {"default_factory": type_}
        else:
            raise MissingTypeError(self.type)

        if self.type == "string":
            if self.min is not None:
                kwargs["min_length"] = self.min
            if self.max is not None:
                kwargs["max_length"] = self.max
        else:
            if issubclass(type_, (ConstrainedFloat, ConstrainedInt)):
                extra: Dict[str, Any] = {}
                if self.min is not None and (type_.ge is None or self.min > type_.ge):
                    extra["ge"] = self.min
                if self.max is not None and (type_.le is None or self.max < type_.le):
                    extra["le"] = self.max

                if extra:
                    kwargs.update({"ge": type_.ge, "le": type_.le, **extra})
                    type_ = type_.mro()[-2]
            else:
                if self.min is not None:
                    kwargs["ge"] = self.min
                if self.max is not None:
                    kwargs["le"] = self.max

        if self.array:
            type_ = List[type_]  # type: ignore
            kwargs["default"] = []
            kwargs.pop("default_factory", None)
        elif self.mapping:
            type_ = Dict[str, type_]  # type: ignore
            kwargs["default"] = {}
            kwargs.pop("default_factory", None)

        if not self.required:
            kwargs["default"] = None
            type_ = Optional[type_]  # type: ignore
            kwargs.pop("default_factory", None)

        return (type_, Field(title=self.title or self.name, description=self.description, **kwargs))


class DataType(DataTypeBase):
    """Interface Control Document."""

    @validator("name", pre=True, always=True)
    def validate_name(cls, value: Any) -> Any:
        """Validate message name."""

        if isinstance(value, str):
            if not is_identifier(value):
                raise ValueError(f"name {value!r} is not a valid identifier")
            if "." not in value and value != "object":
                raise ValueError(f"name {value!r} does not have a namespace")

        return value

    @validator("class_name", pre=True, always=True)
    def validate_class_name(cls, value: Any) -> Any:
        """Validate class name."""

        if isinstance(value, str) and ("." in value or not is_identifier(value)):
            raise ValueError(f"class name {value!r} is not a valid identifier")

        return value

    @validator("fields_", pre=True, always=True)
    def validate_fields(cls, value: Any) -> Any:
        """Validate fields."""

        if not isinstance(value, Sequence):
            return value  # pragma: no cover

        names: Set[str] = {*[]}
        errors: List[ErrorWrapper] = []

        for i, x in enumerate(value):
            if not isinstance(x, Mapping):
                continue  # pragma: no cover
            name = x.get("name", None)
            if name is None:
                continue  # pragma: no cover
            if name in names:
                errors += [ErrorWrapper(ValueError(f"Duplicated name {name!r}"), loc=(i,))]
            else:
                names |= {name}

        if errors:
            raise ValidationError(errors, model=cast(Type[BaseModel], cls))

        return value

    name: str
    version: Optional[str] = None
    class_name: str
    title: Optional[str] = None
    description: Optional[str] = None
    fields_: List[MessageField] = Field(..., alias="fields")

    @classmethod
    def from_file(
        cls,
        path: Union[Path, str],
        file_type: Optional[FileType] = None,
        namespace_root: Optional[Path] = None,
    ) -> List[DataType]:
        """Load DataType from file."""

        if isinstance(path, str):
            path = Path(path)

        path = path.expanduser().resolve()

        if file_type is None:
            file_type = FILE_TYPES.get(path.suffix)

        data: List[Mapping[str, Any]]

        if file_type == FileType.YAML:
            import yaml

            try:
                data = cast(List[Mapping[str, Any]], [*yaml.safe_load_all(path.read_bytes())])
            except yaml.YAMLError as e:
                raise DataTypeError(f"Invalid DataType:\n{indent(str(e), '    ')}")
        elif file_type == FileType.PROTO:
            try:
                from pyrobuf.parse_proto import Proto3Parser
            except ImportError:  # pragma: no cover
                from .vendor.pyrobuf.parse_proto import Proto3Parser  # type: ignore

            try:
                rep = Proto3Parser.parse_from_filename(path, None)
            except Exception as e:
                raise DataTypeError(f"Invalid DataType:\n{indent(str(e), '    ')}")

            match = re.search(r"\bpackage\s+(?P<package>.+)\s*;", path.read_text())
            if not match:
                raise DataTypeError("No package namespace.")
            package = match["package"]
            messages = rep["messages"]
            data = [
                {
                    "name": f"{package}.{message.name}",
                    "class_name": message.name,
                    "fields": [
                        {
                            "name": name,
                            "type": f"{package}.{field.message_name}"
                            if field.type == "message"
                            else field.type,
                            "array": field.modifier == "repeated",
                        }
                        for name, field in message.namespace.items()
                    ],
                }
                for message in messages
            ]
        else:
            raise ValueError(f"Unknown file type: {path}")

        datatypes = [DataType.parse_obj(x) for x in data]

        if namespace_root is not None:
            namespace = ".".join(path.relative_to(namespace_root).parent.parts)
            for datatype in datatypes:
                datatype.name = f"{namespace}.{datatype.name}"

        return datatypes

    def to_model(
        self, models: Optional[Mapping[str, Type[Message]]] = None, module: Optional[str] = None
    ) -> Type[Message]:
        """Generate model from DataType."""

        fields = {field.name: field.get_field_info(models) for field in self.fields_}

        model: Type[Message] = create_model(self.class_name, __base__=Message, **fields)  # type: ignore

        model._TYPE = self.name
        model.__doc__ = self.description or self.title or ""

        if module is not None:
            model.__module__ = f"{module}.{model._TYPE}"

        return model


def resolve(
    datatypes: Sequence[DataType], models: Optional[Mapping[str, Type[Message]]] = None
) -> List[DataType]:
    """Derive resolution order."""

    datatypes = sorted(datatypes, key=attrgetter("name"))

    if models is None:
        models = {}
    else:
        models = {k: v for k, v in flatten(models)}

    result: List[DataType] = []
    seen: Set[str] = {*FIELD_INFO, *models}
    queue: Deque[Tuple[str, DataType]] = deque()
    message_types: Counter_[str] = Counter()

    for datatype in datatypes:
        name = (
            f"{datatype.name}:{datatype.version}" if datatype.version is not None else datatype.name
        )
        message_types[datatype.name] += 1
        queue += [(name, datatype)]

    duplicates = "\n".join(f"{k} ({v})" for k, v in message_types.items() if v > 1)
    if duplicates:
        raise DataTypeError(f"Duplicated message types: {duplicates}")

    deferred = 0

    while queue:
        name, datatype = queue.popleft()

        if all(field.type in seen for field in datatype.fields_):
            seen |= {name, datatype.name}
            result += [datatype]
            deferred = 0
            continue

        queue.append((name, datatype))
        deferred += 1

        if deferred >= len(queue):
            unresolved: DefaultDict[str, List[str]] = defaultdict(list)
            for name, datatype in queue:
                for field in datatype.fields_:
                    if field.type not in seen:
                        unresolved[field.type] += [name]

            missing = ", ".join(
                f"{k!r} ({', '.join(sorted(v))})" for k, v in sorted(unresolved.items())
            )
            raise UnresolvableError(f"Unable to resolve types: {missing}")

    return result
