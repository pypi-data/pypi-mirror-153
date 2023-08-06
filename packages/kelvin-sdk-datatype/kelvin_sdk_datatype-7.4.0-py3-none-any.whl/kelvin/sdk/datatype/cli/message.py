"""Message commands."""

from __future__ import annotations

import subprocess  # nosec
from itertools import chain
from pathlib import Path
from textwrap import indent
from typing import Dict, List, Optional, Sequence

import click
from click.exceptions import Exit

from ..datatype import FILE_TYPES, DataType
from ..package import DEFAULT_MODULE, make_package
from .main import main


@main.group()
def message() -> None:
    """Message Data Models."""


@message.command()
@click.option("--output", "-o", type=Path, help="Output directory.")
@click.option("--namespace-root", "-n", type=Path, help="Namespace root.")
@click.option("--module", "-m", type=str, default=DEFAULT_MODULE, help="Module.")
@click.option("--install", "-i", is_flag=True, help="Install generated package.")
@click.argument("filenames", nargs=-1, type=Path)
def package(
    output: Optional[Path],
    namespace_root: Optional[Path],
    module: str,
    install: bool,
    filenames: Sequence[Path],
) -> None:
    """Generate installable package."""

    datatypes: List[DataType] = []
    errors: Dict[Path, Exception] = {}
    filenames_: List[Path] = []

    if output is not None:
        output = output.resolve().expanduser()

    if namespace_root is not None:
        namespace_root = namespace_root.resolve().expanduser()
        if not namespace_root.is_dir():
            click.echo(f"Namespace root is not a directory: {namespace_root}", err=True)
            raise Exit(1)

    for x in filenames:
        x = x.resolve().expanduser()
        if x.is_file():
            filenames_ += [x]
        elif x.is_dir():
            filenames_ += [
                y
                for y in chain(*(x.glob(f"**/*{ext}") for ext in FILE_TYPES))
                if not any(p.startswith(".") for p in y.parts)
            ]
        else:
            click.echo(f"Not a file/directory: {x}", err=True)
            raise Exit(1)

    click.echo("Reading Data types:")

    for path in filenames_:
        try:
            for datatype in DataType.from_file(path, namespace_root=namespace_root):
                click.echo(f"  █ Loaded Data types: {datatype.name}")
                datatypes += [datatype]
        except Exception as e:
            errors[path] = e

    if errors:
        click.echo("Errors:", err=True)
        for path, ex in errors.items():
            click.echo(
                f"  █ Failed to load Data types: {path}:\n{indent(str(ex), '    ')}", err=True
            )
        raise Exit(1)

    click.echo("\nMaking Module...")
    try:
        package = make_package(datatypes, output, module)
    except Exception as e:  # pragma: no cover
        click.echo(f"  █ Failed to create package: {e}")
        raise Exit(1)

    if install:
        click.echo("\nInstalling Package...")
        rc = subprocess.call(["pip", "-qq", "uninstall", "-y", module])  # nosec
        if rc:  # pragma: no cover
            raise Exit(1)
        rc = subprocess.call(["pip", "-qq", "install", str(package)])  # nosec
        if rc:  # pragma: no cover
            raise Exit(1)
        click.echo("Done")

    click.echo(f"\n{package}")
