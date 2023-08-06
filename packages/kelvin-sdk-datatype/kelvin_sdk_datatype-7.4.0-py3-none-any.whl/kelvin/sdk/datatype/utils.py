"""Utility functions."""

from __future__ import annotations

import os
import re
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from shutil import rmtree
from typing import Any, Dict, Iterator, Mapping, Optional, Tuple

NORMAL_RE = re.compile(r"[^\w]+")
CAMEL_RE = re.compile(r"(^[a-z]|_+[a-zA-Z])")
SNAKE_RE = re.compile(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")


def normalise_name(name: str) -> str:
    """Strip non-word characters from name."""

    return NORMAL_RE.sub("_", name.strip())


def camel_name(name: str) -> str:
    """Create camel-case name from name."""

    return CAMEL_RE.sub(lambda x: x.group(1)[-1].upper(), normalise_name(name))


def snake_name(name: str) -> str:
    """Create underscore-separated name from name."""

    return SNAKE_RE.sub("_", normalise_name(name)).lower()


def is_identifier(name: str) -> bool:
    """Check if identifier is valid."""

    return all(
        x.isidentifier() and not x.startswith("_") and not x.endswith("_") for x in name.split(".")
    )


def flatten(x: Mapping[str, Any], separator: str = ".") -> Iterator[Tuple[str, Any]]:
    """Flatten nested mappings."""

    return (
        (k if not l else f"{k}{separator}{l}", w)
        for k, v in x.items()
        for l, w in (flatten(v) if isinstance(v, Mapping) else [("", v)])
    )


@contextmanager
def chdir(path: Optional[Path]) -> Any:
    """Change working directory and return to previous on exit."""

    if path is None:
        yield
    else:
        prev_cwd = Path.cwd()
        try:
            os.chdir(path if path.is_dir() else path.parent)
            yield
        finally:
            os.chdir(prev_cwd)


def is_protected(path: Path) -> bool:
    """Check if path is protected."""

    for root in [Path.home(), Path.cwd()]:
        try:
            root.relative_to(path)
        except ValueError:
            pass
        else:
            return True

    return False


def safe_rmtree(path: Path) -> None:
    """Remove path only if safe to do so."""

    if is_protected(path):
        raise ValueError(f"Unable to remove protected path: {path}")

    rmtree(path)


def gather(x: Dict[str, Any], key: str) -> Dict[str, Any]:
    """Gather keys from a nested structure."""

    values = x.pop(key, {})

    for v in [*values.values()]:
        values.update(gather(v, key))

    return values


def format_code(code: str, line_length: int = 100) -> str:
    """Format code."""

    import black
    import isort

    return black.format_str(
        isort.code(code, profile="black", known_first_party=["kelvin"], line_length=line_length),
        mode=black.FileMode(string_normalization=True, line_length=line_length),
    )


def to_rfc3339_timestamp(x: datetime) -> str:
    """Convert datetime to RFC-3339 timestamp (UTC)."""

    suffix = "Z" if x.microsecond else ".000000Z"

    return x.astimezone(timezone.utc).replace(tzinfo=None).isoformat() + suffix


def from_rfc3339_timestamp(x: str) -> datetime:
    """Convert RFC-3339 timestamp to datetime (UTC)."""

    if x.endswith("Z"):
        x = f"{x[:-1]}+00:00"

    return datetime.fromisoformat(x).astimezone(timezone.utc)
