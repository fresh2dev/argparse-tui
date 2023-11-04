<h1 align="center">argparse-tui</h1>
<p align="center"><em>Your Argparse CLI, now with a TUI.</em></p>
<h2 align="center">
<a href="https://www.f2dv.com/r/argparse-tui/" target="_blank">Documentation</a>
| <a href="https://www.f2dv.com/s/argparse-tui/" target="_blank">Slide Deck</a>
| <a href="https://www.github.com/fresh2dev/argparse-tui/" target="_blank">Git Repo</a>
</h2>

I was several months into developing my Python CLI framework, [Yapx](https://www.f2dv.com/r/yapx/), when I saw a [post on Hackernews](https://news.ycombinator.com/item?id=36020717) of an awesome tool, [Trogon](https://github.com/Textualize/trogon), which makes it effortless to create a TUI form for a Click CLI app. I was stunned; I knew I had to integrate it into Yapx. But Yapx is built on Python's native Argparse library, not Click. So, I forked Trogon and hacked away until it became this project, *argparse-tui*.

*argparse-tui* can display a TUI of your Python Argparse CLI in one of two ways:

1. Display the TUI form directly:

```python
from argparse import ArgumentParser
from argparse_tui import invoke_tui

parser = ArgumentParser()
...
invoke_tui(parser)
```

2. Add an argument (or command) to the parser that, when provided, displays the TUI form:

```python
from argparse import ArgumentParser
from argparse_tui import add_tui_argument

parser = ArgumentParser()
add_tui_argument(parser)
...
parser.parse_args()
```

In addition to Argparse support, this fork adds some sweet features including:

- Vim-friendly keybindings.
- Redaction of secret values.
- Pre-populating TUI fields with command-line argument values.

<a href="https://www.f2dv.com/s/argparse-tui/" target="_blank">
    <img src="https://img.fresh2.dev/slides_placeholder.png"></img>
</a>

## Install

```
pip install argparse-tui
```

## P.S.

If you appreciate *argparse-tui*, check out [Yapx](https://www.f2dv.com/r/yapx/), [Myke](https://www.f2dv.com/r/myke/), and [TUIview](https://www.f2dv.com/r/tuiview/).

---

[![License](https://img.shields.io/github/license/fresh2dev/argparse-tui?color=blue&style=for-the-badge)](https://www.f2dv.com/r/argparse-tui/license/)
[![GitHub tag (with filter)](https://img.shields.io/github/v/tag/fresh2dev/argparse-tui?filter=!*%5Ba-z%5D*&style=for-the-badge&label=Release&color=blue)](https://www.f2dv.com/r/argparse-tui/changelog/)
[![GitHub last commit (branch)](https://img.shields.io/github/last-commit/fresh2dev/argparse-tui/main?style=for-the-badge&label=updated&color=blue)](https://www.f2dv.com/r/argparse-tui/changelog/)
[![GitHub Repo stars](https://img.shields.io/github/stars/fresh2dev/argparse-tui?color=blue&style=for-the-badge)](https://star-history.com/#fresh2dev/argparse-tui&Date)
[![Funding](https://img.shields.io/badge/funding-%24%24%24-blue?style=for-the-badge)](https://www.f2dv.com/fund/)
<!-- [![GitHub issues](https://img.shields.io/github/issues-raw/fresh2dev/argparse-tui?color=blue&style=for-the-badge)](https://www.github.com/fresh2dev/argparse-tui/issues/) -->
<!-- [![GitHub pull requests](https://img.shields.io/github/issues-pr-raw/fresh2dev/argparse-tui?color=blue&style=for-the-badge)](https://www.github.com/fresh2dev/argparse-tui/pulls/) -->
<!-- [![PyPI - Downloads](https://img.shields.io/pypi/dm/argparse-tui?color=blue&style=for-the-badge)](https://pypi.org/project/argparse-tui/) -->
<!-- [![Docker Pulls](https://img.shields.io/docker/pulls/fresh2dev/argparse-tui?color=blue&style=for-the-badge)](https://hub.docker.com/r/fresh2dev/argparse-tui/) -->
