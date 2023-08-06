"""Generate data-model packages."""

from __future__ import annotations

import atexit
import os
import subprocess  # nosec
import sys
from collections import Counter
from datetime import date
from importlib import import_module
from itertools import chain
from pathlib import Path
from shutil import move
from tempfile import mkdtemp
from textwrap import dedent
from typing import Counter as Counter_
from typing import Dict, List, Optional, Sequence, Type, Union

from .datatype import FILE_TYPES, DataType, resolve
from .exception import DataTypeError
from .message import Message, RawMessage
from .utils import chdir, safe_rmtree

DEFAULT_MODULE = "kelvin.message"
BUILD_FILES = {
    "pyproject.toml": """
        [build-system]
        requires = ["setuptools", "wheel"]
        build-backend = "setuptools.build_meta"
    """,
    "setup.cfg": """
        [metadata]
        name = {name}
        description = Kelvin Message Models
        version = 0.0.0
        url = https://kelvininc.com/
        license = Kelvin Developer SDK License
        license_file = LICENSE.rst
        platform = any

        [options]
        namespace_packages = {namespace}
        packages = find_namespace:
        include_package_data = true
        python_requires = >=3.7.0
        zip_safe = false
        install_requires =
          kelvin-sdk-datatype

        [options.packages.find]
        include = {namespace}.*
    """,
    "LICENSE.rst": """
        *Copyright {today:%Y} Kelvin Inc.*

        Licensed under the Kelvin Inc. Developer SDK License Agreement (the "License");
        you may not use this file except in compliance with the License.  You may
        obtain a copy of the License at:

        `Developer SDK License <http://www.kelvininc.com/developer-sdk-license>`_

        Unless required by applicable law or agreed to in writing, software distributed
        under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OF ANY
        KIND, either express or implied. See the License for the specific language
        governing permissions and limitations under the License.
    """,
    "MANIFEST.in": """
        recursive-include {path} py.typed
    """,
}
INIT_PY = '''
    """Kelvin Message Models."""

    __all__ = [
        "Header",
        "Message",
    ]

    from kelvin.sdk.datatype import Message, Header

    MessageInterface = Message
    HeaderInterface = Header
'''


def make_package(
    datatypes: Sequence[DataType],
    path: Optional[Union[Path, str]] = None,
    module: str = DEFAULT_MODULE,
    wheel: bool = True,
) -> Path:
    """Make message package."""

    models: Dict[str, Type[Message]] = {}
    classes: Counter_[str] = Counter()

    if not any(datatype.name == "object" for datatype in datatypes):
        datatype = DataType(
            name="object",
            version="1.0.0",
            class_name="Object",
            description="Simple data-model",
            fields=[],
        )
        datatypes = [datatype, *datatypes]

    for datatype in resolve(datatypes):
        tag = (
            f"{datatype.name}:{datatype.version}" if datatype.version is not None else datatype.name
        )
        models[tag] = models[datatype.name] = datatype.to_model(models, module)
        classes[f"{datatype.name.rsplit('.')[0]}.{datatype.class_name}"] += 1

    # add raw messages
    models.update((x._TYPE, x) for x in RawMessage.__subclasses__())

    duplicates = sorted(k for k, v in classes.items() if v > 1)
    if duplicates:
        raise DataTypeError(f"Duplicated class names: {', '.join(sorted(duplicates))}")

    data = {
        "name": module.replace(".", "-"),
        "path": module.replace(".", "/"),
        "namespace": module.rsplit(".", 1)[0],
        "today": date.today(),
    }

    keep = True
    if path is None:
        keep = False
        path = Path(mkdtemp())
    elif isinstance(path, str):
        path = Path(path)

    if path.exists():
        if not path.is_dir():
            raise ValueError(f"Path exists and is not a directory: {path}")
    else:
        path.mkdir(parents=True)

    for name, value in BUILD_FILES.items():
        (path / name).write_text(dedent(value.format_map(data).lstrip("\n")))

    if not all(
        x.isidentifier() and not x.startswith("_") and not x.endswith("_")
        for x in module.split(".")
    ):
        raise ValueError(f"Invalid module name: {module}")

    module_path = path / Path(*module.split("."))
    if module_path.exists():
        if not module_path.is_dir():
            raise ValueError(f"Path exists and is not a directory: {path}")
        safe_rmtree(module_path)

    module_path.mkdir(parents=True)

    init_path = module_path / "__init__.py"
    with init_path.open("wt") as file:
        file.write(dedent(INIT_PY).lstrip("\n"))
    (module_path / "py.typed").touch(exist_ok=True)

    for name, model in models.items():
        if ":" in name:
            continue
        head, tail = name.rsplit(".", 1) if "." in name else ("", name)
        sub_module_path = module_path / Path(*head.split("."))
        sub_module_path.mkdir(parents=True, exist_ok=True)

        init_path = sub_module_path / "__init__.py"
        with init_path.open("at" if init_path.exists() else "wt") as init_file:
            init_file.write(f"from .{tail} import {model.__name__}\n")

        model_path = sub_module_path / f"{tail}.py"
        with model_path.open("wt") as model_file:
            if issubclass(model, RawMessage):
                model_file.write(f"from {model.__module__} import {model.__name__}\n")
            else:
                model_file.write(model.to_code())

    if not wheel:
        return path

    args = [
        "pip",
        "-q",
        "wheel",
        "--no-deps",
        "--no-build-isolation",
        f"--wheel-dir={path}",
        str(path),
    ]

    with chdir(path):
        subprocess.call(args)  # nosec

    wheels = [*path.glob(f"{module.replace('.', '_')}-*.whl")]

    if not wheels:
        raise DataTypeError("No wheel created")  # pragma: no cover

    result = sorted(wheels, key=lambda x: x.stat().st_mtime, reverse=True)[0]

    if not keep:
        dest = Path.cwd() / result.name
        move(str(result), dest)
        result = dest
        safe_rmtree(path)

    return result


def load_datatypes(
    directory: Union[Path, str],
    module: str = DEFAULT_MODULE,
    namespace_root: Optional[Path] = None,
    verbose: bool = False,
) -> None:
    """Load Data types from directory."""

    if isinstance(directory, str):
        directory = Path(directory)
    elif not isinstance(directory, Path):
        raise TypeError("DataType directory must be a path or string")

    directory = directory.expanduser().resolve()

    if not directory.is_dir():
        raise ValueError(f"Not a directory: {directory}")

    file = sys.stderr if verbose else open(os.devnull, "w")

    datatypes: List[DataType] = []

    print(f"Loading Data types: {directory}", file=file)

    for path in chain(*(directory.glob(f"**/*{ext}") for ext in FILE_TYPES)):
        print(f"  - {path.relative_to(directory)}:", file=file)
        for datatype in DataType.from_file(path, namespace_root=namespace_root):
            print(f"    + {datatype.name}", file=file)
            datatypes += [datatype]

    module_dir = make_package(datatypes, module=module, wheel=False)
    atexit.register(safe_rmtree, module_dir)
    sys.path.insert(0, str(module_dir))

    # trigger cache load
    for datatype in resolve(datatypes):
        import_module(f"{module}.{datatype.name}")
