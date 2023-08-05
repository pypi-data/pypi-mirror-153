"""A simple example of a pure python provider"""
from __future__ import annotations

import dataclasses
import itertools
import pathlib
from typing import Iterable, List, Optional


@dataclasses.dataclass(frozen=True)
class GreetingCommand:
    name: str
    help: Optional[str]
    subject: str

    def __call__(self, args: List[str]) -> None:
        print(f"Hello {self.subject.capitalize()}!")
        # pylint: disable=no-self-use
        if args:
            print(f"I see you brought {args[1].capitalize()}.")
        else:
            print("Are you the brain specialist?")


class GreetingProvider:
    # pylint: disable=too-few-public-methods

    def __init__(self, cwd: pathlib.Path) -> None:
        self._cwd = cwd

    def v1_commands(self) -> Iterable[GreetingCommand]:
        for path in itertools.chain([self._cwd], self._cwd.parents):
            if path.parent.name == "home":
                yield GreetingCommand("greet", "Say hello", path.name)
                return
