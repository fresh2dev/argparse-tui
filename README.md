<h1 align="center">argparse-tui</h1>
<p align="center"><em>Present your Argparse CLI as a Textual UI (TUI).</em></p>
<h2 align="center">
<a href="https://www.f2dv.com/r/argparse-tui/" target="_blank">Documentation</a>
| <a href="https://www.github.com/fresh2dev/argparse-tui/" target="_blank">Git Repo</a>
</h2>

`argparse-tui` is a Python package that can convert your Argparse CLI into a Textual UI (TUI). It is also able to provide a TUI interface to existing command-line apps using Argparse as a declarative DSL. This library is a soft-fork of [Trogon](https://github.com/Textualize/trogon), powered by the [Textual TUI framework](https://github.com/textualize/textual), refactored for use with Python's native *Argparse*, instead of *Click*.

______________________________________________________________________

<!-- TOC GFM -->

- [Distinguishing Features](#distinguishing-features)
    - [Vim-friendly Nav](#vim-friendly-nav)
    - [Redaction](#redaction)
    - [Pre-populating TUI](#pre-populating-tui)
- [Use](#use)
- [Examples](#examples)
- [Install](#install)
- [Related Projects](#related-projects)

<!-- /TOC -->

______________________________________________________________________

![](https://img.fresh2.dev/1691530009_42873ae0cbe.png){: style="width:60%;border:1px solid gray"}

## Distinguishing Features

This package also has these distinguishing features from it's upstream relative, Trogon:

### Vim-friendly Nav

- Move down / up using `j` / `k`.
- `/` to focus search.
- `Enter` to focus the selected command.
- `Escape` to focus the command-tree.
- `Ctrl+y` to copy the current command.

### Redaction

Redact sensitive values in the TUI by including the term `<secret>` in the argument's help text.

```python
parser.add_argument("-p", "--password", help="<secret>")
```

![](https://img.fresh2.dev/1691520889_8d13165a60d.png){: style="width:60%;border:1px solid gray"}

### Pre-populating TUI

Command-line args are used to filter and pre-populate the TUI form.

```shell
$ awesome-app hello world --tui
```

![](https://img.fresh2.dev/1691516124_211d67f1ea7.png){: style="width:60%;border:1px solid gray"}

## Use

*argparse-tui* can display a TUI of your Python Argparse CLI in one of two ways:

1. Add an argument (or command) to a parser that, when provided, displays the TUI form:

```python
from argparse import ArgumentParser
from argparse_tui import add_tui_argument

parser = ArgumentParser()
add_tui_argument(parser)
...
parser.parse_args()
```

> This is useful when your CLI app is powered by Argparse and you want to display it as a Textual UI.

1. Display the TUI form directly:

```python
from argparse import ArgumentParser
from argparse_tui import invoke_tui

parser = ArgumentParser()
...
invoke_tui(parser)
```

> This is useful when you are using Argparse as a declarative DSL to build a TUI which models an existing CLI application.

## Examples

Example scripts for Argparse, Yapx, are provided in the [`examples/`](https://github.com/fresh2dev/argparse-tui/tree/main/examples) directory.

## Install

```
pip install argparse-tui
```

## Related Projects

- [fresh2dev/TUIview](https://www.f2dv.com/r/tuiview/) is a Python CLI that uses argparse-tui TUIs for existing CLI applications.

- [fresh2dev/yapx](https://www.f2dv.com/r/yapx/) is a Python library for building a Python CLI from your existing Python functions, with `argparse-tui` support built-in.

- [fresh2dev/myke](https://www.f2dv.com/r/myke/) is a Python CLI that builds on argparse-tui and Yapx to serve as a task runner with a CLI and TUI interface.

______________________________________________________________________

[![License](https://img.shields.io/github/license/fresh2dev/argparse-tui?color=blue&style=for-the-badge)](https://www.f2dv.com/r/argparse-tui/license/)
[![GitHub tag (with filter)](https://img.shields.io/github/v/tag/fresh2dev/argparse-tui?filter=!*%5Ba-z%5D*&style=for-the-badge&label=Release&color=blue)](https://www.f2dv.com/r/argparse-tui/changelog/)
[![GitHub last commit (branch)](https://img.shields.io/github/last-commit/fresh2dev/argparse-tui/main?style=for-the-badge&label=updated&color=blue)](https://www.f2dv.com/r/argparse-tui/changelog/)
[![GitHub Repo stars](https://img.shields.io/github/stars/fresh2dev/argparse-tui?color=blue&style=for-the-badge)](https://star-history.com/#fresh2dev/argparse-tui&Date)

<!-- [![Funding](https://img.shields.io/badge/funding-%24%24%24-blue?style=for-the-badge)](https://www.f2dv.com/fund/) -->

<!-- [![GitHub issues](https://img.shields.io/github/issues-raw/fresh2dev/argparse-tui?color=blue&style=for-the-badge)](https://www.github.com/fresh2dev/argparse-tui/issues/) -->

<!-- [![GitHub pull requests](https://img.shields.io/github/issues-pr-raw/fresh2dev/argparse-tui?color=blue&style=for-the-badge)](https://www.github.com/fresh2dev/argparse-tui/pulls/) -->

<!-- [![PyPI - Downloads](https://img.shields.io/pypi/dm/argparse-tui?color=blue&style=for-the-badge)](https://pypi.org/project/argparse-tui/) -->

<!-- [![Docker Pulls](https://img.shields.io/docker/pulls/fresh2dev/argparse-tui?color=blue&style=for-the-badge)](https://hub.docker.com/r/fresh2dev/argparse-tui/) -->
