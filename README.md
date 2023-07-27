# argparse-tui

> Display your Python argparse parser as a TUI.

| Links         |                                               |
|---------------|-----------------------------------------------|
| Code Repo     | https://www.github.com/fresh2dev/argparse-tui |
| Mirror Repo   | https://www.f2dv.com/r/argparse-tui           |
| Documentation | https://www.f2dv.com/r/argparse-tui           |
| Changelog     | https://www.f2dv.com/r/argparse-tui/changelog |
| License       | https://www.f2dv.com/r/argparse-tui/license   |
| Funding       | https://www.f2dv.com/fund                     |

[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/fresh2dev/argparse-tui?color=blue&style=for-the-badge)](https://www.f2dv.com/r/argparse-tui/changelog)
[![GitHub Release Date](https://img.shields.io/github/release-date/fresh2dev/argparse-tui?color=blue&style=for-the-badge)](https://www.f2dv.com/r/argparse-tui/changelog)
[![License](https://img.shields.io/github/license/fresh2dev/argparse-tui?color=blue&style=for-the-badge)](https://www.f2dv.com/r/argparse-tui/license)
[![GitHub Repo stars](https://img.shields.io/github/stars/fresh2dev/argparse-tui?color=blue&style=for-the-badge)](https://star-history.com/#fresh2dev/argparse-tui&Date)
[![GitHub issues](https://img.shields.io/github/issues-raw/fresh2dev/argparse-tui?color=blue&style=for-the-badge)](https://www.github.com/fresh2dev/argparse-tui/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr-raw/fresh2dev/argparse-tui?color=blue&style=for-the-badge)](https://www.github.com/fresh2dev/argparse-tui/pulls)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/argparse-tui?color=blue&style=for-the-badge)](https://pypi.org/project/argparse-tui)
[![Docker Pulls](https://img.shields.io/docker/pulls/fresh2dev/argparse-tui?color=blue&style=for-the-badge)](https://hub.docker.com/r/fresh2dev/argparse-tui)
[![Changelog](https://img.shields.io/website?down_message=unavailable&label=docs&style=for-the-badge&up_color=blue&up_message=available&url=https://www.f2dv.com/r/argparse-tui/changelog)](https://www.f2dv.com/r/argparse-tui/changelog)
[![Funding](https://img.shields.io/badge/funding-%24%24%24-blue?style=for-the-badge)](https://www.f2dv.com/fund)

---

## Overview

This is a fork of the Textualize [Trogon TUI library](https://github.com/Textualize/trogon.git) that introduces these features:

- add support for Python's argparse parsers
    - add `--tui` flag as an argument
    - or, add `tui` command to your subparser
    - or, invoke the TUI with `invoke_tui(parser)`
- remove support for Click
- add ability for TUI parameter to filter subcommands
- support for manually constructing schemas
- support for argparse
- add examples for yapx, myke, and sys.argv
- support ommission of hidden parameters and subcommands from the TUI
- support the redaction of sensitive "secret" values
- support for showing required prompts as read-only
- ability to join list arguments values like this: `-x 1 -x 2 -x 3` (default), or like this: `-x 1 2 3`
- vim-friendly keybindings

## Install

Install from PyPI:

```
pip install argparse-tui
```

## Use

```python
import arparse
from argparse_tui import add_tui_argument, add_tui_command

parser = argparse.ArgumentParser()

# Add tui argument (my-cli --tui)
add_tui_argument(parser, option_strings=["--tui"], help="Open Textual UI")

# Or, add tui command (my-cli tui)
add_tui_command(parser, command="tui", help="Open Textual UI")

parser.print_help()
```

### `invoke_tui`

argparse-tui offers this function to display a TUI based on the arguments of the given parser:

```python
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
```

In this way, `argparse` is not actually serving as an argument parser, but instead as the specification language for the TUI. Whoa.

### ChatGPT and TUIview

Given the structured help text output of some CLI program, it turns out ChatGPT is decent at implementing an equivalent CLI using a Python argparse parser. Whoaaa.

Coupled with `invoke_tui`, this means that argparse-tui is capable of producing a TUI for any CLI. This is the idea behind a tool built using argparse-tui: [TUIview](https://github.com/fresh2dev/tuiview). It does not use ChatGPT itself, but I used ChatGPT to generate equivalent-enough argparse parsers for `git`, `rsync`, `grep`.

## Docs

See more examples in the [reference docs](https://www.f2dv.com/r/argparse-tui/reference).


## Support

*Brought to you by...*

<a href="https://www.f2dv.com"><img src="https://img.fresh2.dev/fresh2dev.svg" style="filter: invert(50%);"></img></a>
