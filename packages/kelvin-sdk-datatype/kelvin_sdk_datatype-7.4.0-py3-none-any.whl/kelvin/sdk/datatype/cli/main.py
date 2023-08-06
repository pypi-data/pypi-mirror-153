"""Main command."""

import sys
from pathlib import Path
from typing import Any, Callable, List, Optional, Union

import click
import xdg
from click import Context
from click import Group as _Group
from click_shell import Shell

COMMAND = Path(sys.argv[0]).stem


def _prompt(ctx: Context) -> str:
    """Build prompt."""

    result: List[str] = [""]

    root = ctx
    while root.parent:
        result += [root.command.name]  # type: ignore
        root = root.parent
    result += [COMMAND]

    return " > ".join(reversed(result))


class Group(Shell):
    """Click Shell."""

    def __init__(
        self,
        prompt: Optional[Union[str, Callable[[Context], str]]] = _prompt,
        intro: Optional[str] = None,
        hist_file: Optional[str] = None,
        on_finished: Optional[Callable[[Context], None]] = None,
        **kwargs: Any,
    ) -> None:
        """Initialise click shell."""

        if hist_file is None:
            hist_file = str(Path(xdg.xdg_data_home()) / "kelvin" / f"{COMMAND}-history")

        super().__init__(
            prompt=prompt, intro=intro, hist_file=hist_file, on_finished=on_finished, **kwargs
        )

    def group(self, *args: Any, **kwargs: Any) -> Callable[[Callable[..., Any]], _Group]:
        """
        A shortcut decorator for declaring and attaching a group to
        the group.  This takes the same arguments as :func:`group` but
        immediately registers the created command with this instance by
        calling into :meth:`add_command`.
        """

        kwargs.setdefault("cls", type(self))

        kwargs.setdefault("prompt", self.shell.prompt)
        kwargs.setdefault("intro", self.shell.intro)
        kwargs.setdefault("hist_file", self.shell.hist_file)
        kwargs.setdefault("on_finished", self.shell.on_finished)

        return super().group(*args, **kwargs)


@click.group(cls=Group)
def main() -> None:
    """Kelvin DataType CLI."""
