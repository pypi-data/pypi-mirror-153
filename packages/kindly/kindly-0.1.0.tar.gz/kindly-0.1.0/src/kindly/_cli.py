import argparse
import functools
import logging
import os
import pathlib
import subprocess
from typing import Callable, List

import pkg_resources

from kindly import api

logger = logging.getLogger(__name__)


def _wrapped(func: Callable[[List[str]], None]) -> Callable[[argparse.Namespace], None]:
    @functools.wraps(func)
    def inner(args: argparse.Namespace) -> None:
        func(args.args)

    return inner


def _parser(cwd: pathlib.Path) -> argparse.ArgumentParser:
    program_parser = argparse.ArgumentParser()
    program_subparsers = program_parser.add_subparsers(required=True)

    # TODO: Define strategy for dealing with conflicts
    # Maybe enable the user to disable (distribution,command) tuples in the tools
    # section of pyproject.toml.
    # One distrigution could still provide the same command multiple times (this
    # distribution provides any command that the user specifies in the aliases
    # file); this should probably be an error.

    for entry_point in pkg_resources.iter_entry_points("kindly.provider"):
        cls = entry_point.load()
        provider: api.Provider = cls(cwd)
        for command in provider.v1_commands():
            command_parser = program_subparsers.add_parser(
                command.name,
                help=command.name.capitalize().replace("_", " ")
                if command.help is None
                else command.help,
            )
            command_parser.add_argument("args", nargs="*")
            command_parser.set_defaults(func=_wrapped(command))

    return program_parser


def cli(cwd: pathlib.Path, args: List[str]) -> None:
    # noinspection PyUnresolvedReferences
    # pylint: disable=protected-access
    logging.basicConfig(level=logging._nameToLevel[os.environ.get("LEVEL", "WARNING")])
    parser = _parser(cwd)
    parsed = parser.parse_args(args)
    try:
        parsed.func(parsed)
    except subprocess.SubprocessError:
        parser.exit(1)
