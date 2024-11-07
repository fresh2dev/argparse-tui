#!/usr/bin/env python3
import argparse
import sys

from argparse_tui import invoke_tui

parser = argparse.ArgumentParser(prog="echo")

parser.add_argument("STRING", nargs="*")


parser.add_argument("-e", "--email", help="Email address")
parser.add_argument(
    "-n",
    action="store_true",
    help="do not output the trailing newline",
)

invoke_tui(parser, cli_args=sys.argv[1:])
