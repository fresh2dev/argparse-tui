# argparse-tui

> Display your Python argparse CLI as a TUI.

| Links         |                                                      |
|---------------|------------------------------------------------------|
| Code Repo     | https://www.github.com/fresh2dev/argparse-tui        |
| Mirror Repo   | https://www.f2dv.com/code/r/argparse-tui             |
| Documentation | https://www.f2dv.com/code/r/argparse-tui/i           |
| Changelog     | https://www.f2dv.com/code/r/argparse-tui/i/changelog |
| License       | https://www.f2dv.com/code/r/argparse-tui/i/license   |
| Funding       | https://www.f2dv.com/fund                            |

[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/fresh2dev/argparse-tui?color=blue&style=for-the-badge)](https://www.github.com/fresh2dev/argparse-tui/releases)
[![GitHub Release Date](https://img.shields.io/github/release-date/fresh2dev/argparse-tui?color=blue&style=for-the-badge)](https://www.github.com/fresh2dev/argparse-tui/releases)
[![License](https://img.shields.io/github/license/fresh2dev/argparse-tui?color=blue&style=for-the-badge)](https://www.f2dv.com/code/r/argparse-tui/i/license)
[![GitHub issues](https://img.shields.io/github/issues-raw/fresh2dev/argparse-tui?color=blue&style=for-the-badge)](https://www.github.com/fresh2dev/argparse-tui/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr-raw/fresh2dev/argparse-tui?color=blue&style=for-the-badge)](https://www.github.com/fresh2dev/argparse-tui/pulls)
[![GitHub Repo stars](https://img.shields.io/github/stars/fresh2dev/argparse-tui?color=blue&style=for-the-badge)](https://star-history.com/#fresh2dev/argparse-tui&Date)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/argparse-tui?color=blue&style=for-the-badge)](https://pypi.org/project/argparse-tui)
[![Docs Website](https://img.shields.io/website?down_message=unavailable&label=docs&style=for-the-badge&up_color=blue&up_message=available&url=https://www.f2dv.com/code/r/argparse-tui/i)](https://www.f2dv.com/code/r/argparse-tui/i)
[![Coverage Website](https://img.shields.io/website?down_message=unavailable&label=coverage&style=for-the-badge&up_color=blue&up_message=available&url=https://www.f2dv.com/code/r/argparse-tui/i/tests/coverage)](https://www.f2dv.com/code/r/argparse-tui/i/tests/coverage)
[![Funding](https://img.shields.io/badge/funding-%24%24%24-blue?style=for-the-badge)](https://www.f2dv.com/fund)

---

## Overview

This is a fork of the Textualize [Trogon TUI library](https://github.com/Textualize/trogon.git) that introduces these features:

- add support for Python's argparse parsers
- remove support for Click
- add ability for TUI parameter to filter subcommands
- support for manually constructing schemas
- support for argparse
- add examples for yapx, myke, and sys.argv
- support ommission of hidden parameters and subcommands from the TUI
- support the redaction of sensitive "secret" values
- support for showing required prompts as read-only
- positional arguments come before keyword arguments in the generated command
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

## Docs

See more examples in the [reference docs](https://www.f2dv.com/code/r/argparse-tui/i/reference/).


## Support

*Brought to you by...*

<a href="https://www.f2dv.com"><img src="https://img.fresh2.dev/fresh2dev.svg" style="filter: invert(50%);"></img></a>
