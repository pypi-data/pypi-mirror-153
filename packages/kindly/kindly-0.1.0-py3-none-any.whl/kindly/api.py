"""Specification of public interface for plugins"""
from __future__ import annotations

import pathlib
import sys
from typing import Iterable, List, Optional

if sys.version_info[1] < 8:
    from typing_extensions import Protocol
else:
    from typing import Protocol


class V1Command(Protocol):
    @property
    def name(self) -> str:
        """Return name of command"""

    @property
    def help(self) -> Optional[str]:
        """Return help message, if any

        If None is returned the help message will be chosen by kindly.
        """

    def __call__(self, args: List[str]) -> None:
        """Implementation of the command

        Receives any arguments that were not consumed by parsing.
        """


class Provider(Protocol):
    # pylint: disable=too-few-public-methods
    def __init__(self, cwd: pathlib.Path) -> None:
        ...

    def v1_commands(self) -> Iterable[V1Command]:
        ...

    # It would be nice with a bit more interactivity.
    # v2 will probably delegate parsing to providers.
    # v3 will probably delegate parsing and tab completion to providers.
