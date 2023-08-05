"""Lets the user specify path dependend aliases"""
from __future__ import annotations

import ast
import dataclasses
import itertools
import pathlib
import shlex
import subprocess
from typing import Dict, Iterable, List, Optional, Tuple


def _find_upwards(start: pathlib.Path, name: str) -> pathlib.Path:
    for parent in itertools.chain([start], start.parents):
        path = parent / name
        if path.exists():
            return path
    raise FileNotFoundError


@dataclasses.dataclass(frozen=True)
class AliasCommand:
    cwd: pathlib.Path
    name: str
    help: Optional[str]
    steps: Tuple[Tuple[str, ...], ...]

    def __call__(self, args: List[str]) -> None:
        for step in self.steps:
            subprocess.check_call(step + tuple(args), cwd=self.cwd)

    @staticmethod
    def from_spec(cwd: pathlib.Path, name: str, spec: Dict) -> AliasCommand:
        try:
            raw_steps = spec["steps"]
        except KeyError:
            raw_steps = [spec["step"]]

        steps = [
            shlex.split(step) if isinstance(step, str) else step for step in raw_steps
        ]

        # Would be nice to extend this to allow containerized commands akin to jobs in
        # github workflows.

        return AliasCommand(
            cwd=cwd,
            name=name,
            help=spec.get("help", name.capitalize().replace("_", " ")),
            steps=tuple(map(tuple, steps)),
        )


class AliasesProvider:
    # pylint: disable=too-few-public-methods

    def __init__(self, cwd: pathlib.Path) -> None:
        self._cwd = cwd

    def v1_commands(self) -> Iterable[AliasCommand]:
        try:
            kindly_pyi = _find_upwards(pathlib.Path.cwd(), "kindly_aliases.pyl")
        except FileNotFoundError:
            return

        raw_commands = ast.literal_eval(kindly_pyi.read_text())["commands"]
        for name, spec in raw_commands.items():
            yield AliasCommand.from_spec(self._cwd, name, spec)
