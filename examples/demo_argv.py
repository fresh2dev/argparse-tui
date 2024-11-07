#!/usr/bin/env python3

from __future__ import annotations

import sys

from argparse_tui import Tui
from argparse_tui.constants import DEFAULT_COMMAND_NAME
from argparse_tui.schemas import (
    ArgumentSchema,
    CommandName,
    CommandSchema,
    OptionSchema,
)

root_schema: CommandSchema = CommandSchema(
    name=CommandName("hello"),
    docstring="just sayin'",
    options=[
        OptionSchema(
            name=["--name"],
            default="world",
        ),
        OptionSchema(
            name=["-u", "--to-upper"],
            type=bool,
            is_flag=True,
        ),
        OptionSchema(name=["-t", "--test"], type=int, choices=[1, 2, 3]),
        OptionSchema(
            name=["-s", "--subjects"],
            type=str,
            multiple=True,
            multi_value=True,
        ),
    ],
    arguments=[
        ArgumentSchema(name=["subjects"], type=str, multiple=True, multi_value=True),
    ],
)

subcmd_1: CommandSchema = CommandSchema(
    name=CommandName("wat"),
    arguments=[
        ArgumentSchema(name="anything", help="wat!"),
    ],
    options=[
        OptionSchema(
            name=["--name"],
            default="world",
        ),
        OptionSchema(
            name=["--to-upper"],
            type=bool,
            is_flag=True,
        ),
    ],
)

tui: Tui = Tui.from_schemas(root_schema, subcmd_1, app_name=None)

if __name__ == "__main__":
    if DEFAULT_COMMAND_NAME in sys.argv[1:]:
        tui.run()
    else:
        print(sys.argv)
