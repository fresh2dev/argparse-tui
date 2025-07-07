import os

if "TEXTUAL_THEME" not in os.environ:
    os.environ["TEXTUAL_THEME"] = "catppuccin-mocha"


from .__version__ import __version__
from .argparse import (
    TuiAction,
    add_tui_argument,
    add_tui_command,
    build_tui,
    invoke_tui,
)
from .tui import Tui

__all__ = [
    "Tui",
    "TuiAction",
    "__version__",
    "add_tui_argument",
    "add_tui_command",
    "build_tui",
    "invoke_tui",
]
