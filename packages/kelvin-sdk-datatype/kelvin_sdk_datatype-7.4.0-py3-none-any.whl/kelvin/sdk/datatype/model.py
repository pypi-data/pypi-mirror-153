"""Base Model."""

from __future__ import annotations

import json
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import date
from functools import wraps
from operator import attrgetter
from time import time_ns
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Generic,
    Iterator,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

import orjson
from orjson import OPT_SERIALIZE_NUMPY, OPT_SORT_KEYS
from pydantic import BaseConfig, BaseModel, Extra, Field, validator
from pydantic.json import pydantic_encoder
from pydantic.main import ModelMetaclass
from pydantic.schema import default_ref_template

if TYPE_CHECKING:
    from IPython.lib.pretty import PrettyPrinter
else:
    PrettyPrinter = Any

_TIMESTAMP: ContextVar[Callable[[], int]] = ContextVar("timestamp")


@contextmanager
def timestamper(f: Callable[[], int]) -> Any:
    """Context handler for timestamping."""

    token = _TIMESTAMP.set(f)

    try:
        yield f
    finally:
        _TIMESTAMP.reset(token)


class ModelMeta(ModelMetaclass):
    """BaseModel metaclass."""


class Model(BaseModel, MutableMapping[str, Any], metaclass=ModelMeta):
    """Base Model."""

    class Config(BaseConfig):
        """Pydantic config."""

        extra = Extra.forbid
        validate_assignment = True

    def __repr__(self) -> str:
        """Return a string represenation."""

        name = type(self).__name__

        return super().__repr__().replace(name, f"<{name}>", 1)

    def _pretty_items(self) -> Iterator[Tuple[str, Any]]:
        """Pretty items."""

        yield from self._iter()

    def _repr_pretty_(self, p: PrettyPrinter, cycle: bool) -> None:
        """Pretty representation."""

        name = type(self).__name__

        with p.group(4, f"<{name}>(", ")"):
            if cycle:  # pragma: no cover
                p.text("...")
                return

            for i, (k, v) in enumerate(self._pretty_items()):
                if i:
                    p.text(",")
                    p.breakable()
                else:
                    p.breakable("")
                p.text(f"{k}=")
                p.pretty(f"{v}" if isinstance(v, date) else v)

    def __getitem__(self, name: str) -> Any:
        """Get item."""

        if name.startswith("_"):
            raise KeyError(name) from None

        if "." not in name:
            return self.__dict__[name]

        head, tail = name.split(".", 1)
        try:
            data = self.__dict__[head]
        except KeyError:
            raise KeyError(head) from None

        if not isinstance(data, Model):
            raise TypeError(f"{type(data).__name__!r} object at {head!r} is not a model")

        try:
            return data[tail]
        except KeyError:
            raise KeyError(name) from None

    def __setitem__(self, name: str, value: Any) -> None:
        """Set item."""

        if "." not in name:
            try:
                return setattr(self, name, value)
            except ValueError:
                raise KeyError(name) from None

        head, tail = name.rsplit(".", 1)
        try:
            data = attrgetter(head)(self)
        except AttributeError:
            raise KeyError(head) from None

        if not isinstance(data, Model):
            raise TypeError(f"{type(data).__name__!r} object at {head!r} is not a model") from None

        try:
            return setattr(data, tail, value)
        except ValueError:
            raise KeyError(name) from None

    def __delitem__(self, name: str) -> None:
        """Delete item."""

        if "." not in name:
            try:
                return delattr(self, name)
            except AttributeError:
                raise KeyError(name) from None

        head, tail = name.rsplit(".", 1)
        try:
            data = attrgetter(head)(self)
        except AttributeError:
            raise KeyError(head) from None

        if not isinstance(data, Model):
            raise TypeError(f"{type(data).__name__!r} object at {head!r} is not a model") from None

        try:
            return delattr(data, tail)
        except AttributeError:
            raise KeyError(name) from None

    def __len__(self) -> int:
        """Length of items."""

        return len(self.__dict__)

    def __iter__(self) -> Iterator[str]:  # type: ignore
        """Key iterator."""

        return iter(self.__dict__)

    def __hash__(self) -> int:
        """Hash for uniqueness."""

        return hash(self.json())


class CoreHeader(Model):
    """Core Header."""

    @validator("time_of_validity", pre=True, always=True)
    def validate_time_of_validity(cls, value: Optional[int]) -> int:
        """Validate time of validity."""

        return value if value is not None else _TIMESTAMP.get(time_ns)()

    time_of_validity: int = Field(
        None,
        title="Time of Validity",
        description="Time of message validity.",
        ge=0,
    )

    def __hash__(self) -> int:
        """Hash for uniqueness."""

        return hash(self.json())


class CoreModelMeta(ModelMeta):
    """Core Model meta-class."""

    _header_type: Type[CoreHeader]

    def __new__(
        metacls: Type[CoreModelMeta], name: str, bases: Tuple[Type, ...], __dict__: Dict[str, Any]
    ) -> CoreModelMeta:
        """Create model class."""

        cls = cast(CoreModelMeta, super().__new__(metacls, name, bases, __dict__))

        if "__orig_bases__" in __dict__:
            cls._header_type = __dict__["__orig_bases__"][-1].__args__[0]

        return cls


T = TypeVar("T", bound=CoreHeader)
S = TypeVar("S", bound="CoreModel", covariant=True)


class CoreModel(Model, Generic[T], metaclass=CoreModelMeta):
    """Core Model."""

    _: T

    _header_type: Type[T]

    __slots__ = ("_", "_header_type")

    def __init__(self, _: Optional[Union[T, Mapping[str, Any]]] = None, **kwargs: Any) -> None:
        """Initialise message."""

        if _ is not None:
            if isinstance(_, self._header_type):
                pass
            elif isinstance(_, Mapping):
                _ = self._header_type.parse_obj(_)
            else:
                raise ValueError(f"Invalid header type: {type(_).__name__!r}") from None
        else:
            _ = self._header_type()

        object.__setattr__(self, "_", _)

        # allow sub-fields to use the same timestamp
        time_of_validity = _.time_of_validity  # type: ignore

        with timestamper(lambda: time_of_validity):
            super().__init__(**kwargs)

    def __reduce__(self) -> Tuple[Any, ...]:
        """Reduce data for pickling."""

        result = cast(Tuple[Any, ...], super().__reduce__())

        result[-1]["__private_attribute_values__"]["_"] = self._

        return result

    def __eq__(self, value: Any) -> bool:
        """Equality."""

        if not isinstance(value, type(self)):
            return False

        return self._ == value._ and all(v == getattr(value, k, ...) for k, v in self._iter())

    @classmethod
    def _convert(cls, x: Any, header: bool = True) -> Any:
        """Convert input to standard Python types."""

        if x is None or isinstance(x, (str, int, float)):
            return x

        if isinstance(x, CoreModel):
            return x._lower(header)

        if isinstance(x, Mapping):
            return {k: cls._convert(v, header) for k, v in x.items()}

        if isinstance(x, Sequence):
            return [cls._convert(v, header) for v in x]

        raise ValueError(f"Unlowerable type {type(x).__name__!r}")  # pragma: no cover

    def _lower(self, header: bool = True) -> Dict[str, Any]:
        """Convert to standard Python types."""

        result = dict(self._iter(by_alias=True, exclude_none=True, exclude_unset=True))
        result["_"] = self._.dict(exclude_none=True)

        return self._convert(result, header)

    def encode(self, header: bool = True) -> bytes:
        """Encode model."""

        return orjson.dumps(self._lower(header), option=OPT_SERIALIZE_NUMPY | OPT_SORT_KEYS)

    @classmethod
    def decode(cls: Type[S], data: bytes) -> S:
        """Decode model."""

        return cls.parse_raw(data)

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

    def __deepcopy__(self: S, memo: Dict[int, S]) -> S:
        """Deep copy."""

        key = id(self)

        result = memo.get(key)
        if result is not None:
            return result  # pragma: no cover

        result = self.copy(deep=True)
        object.__setattr__(result, "_", self._.copy())

        memo[key] = result

        return result

    @wraps(BaseModel.copy)
    def copy(self: S, *args: Any, **kwargs: Any) -> S:
        """Copy model."""

        result = super().copy(*args, **kwargs)
        object.__setattr__(result, "_", self._.copy())

        return result

    @property
    def header(self) -> CoreHeader:
        """Header."""

        return self._

    @wraps(BaseModel.schema)
    @classmethod
    def schema_json(
        cls, *, by_alias: bool = True, ref_template: str = default_ref_template, **dumps_kwargs: Any
    ) -> str:
        """Generate schema as JSON."""

        return json.dumps(
            cls.schema(by_alias=by_alias, ref_template=ref_template),
            default=pydantic_encoder,
            **dumps_kwargs,
        )

    def __hash__(self) -> int:
        """Hash for uniqueness."""

        return hash(self.encode())
