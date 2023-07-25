import argparse

from argparse_tui import invoke_tui

parser = argparse.ArgumentParser(prog="echo")

parser.add_argument("STRING", nargs="*")

parser.add_argument(
    "-n",
    action="store_true",
    help="do not output the trailing newline",
)

invoke_tui(parser)
