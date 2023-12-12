import argparse

import pytest
from textual.app import App

from argparse_tui.argparse import build_tui


@pytest.mark.asyncio()
async def test_app():
    parser = argparse.ArgumentParser()
    _ = parser.add_argument("pos_arg")
    _ = parser.add_argument("--flag", action="store_true")
    _ = parser.add_argument("--multiple", action="append")
    _ = parser.add_argument("--multi-value", nargs="+")
    _ = parser.add_argument("--value")

    subparsers = parser.add_subparsers()
    _ = subparsers.add_parser("command1")
    _ = subparsers.add_parser("command2")

    app: App = build_tui(parser)

    async with app.run_test() as pilot:
        await pilot.press("q")
