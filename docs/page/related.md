# Related Projects

## [Trogon](https://github.com/Textualize/trogon)

This project started from the Textualize Trogon library, which is currently specific to Click.

I forked the project to make it specific to Python's native `argparse` and to add some extra sugar.

## [Textual](https://github.com/Textualize/textual)

Textual is the Python TUI framework that powers Trogon and argparse-tui.

## [TUIview](https://www.f2dv.com/code/r/tuiview/i/)

TUIview is a tool (`tv`) built using argparse-tui that displays a Textual UI for a variety of common CLI tools.

## Integrations

### [Yapx](https://www.f2dv.com/code/r/yapx/i/)

Yapx is a CLI library built on top of argparse which makes it easy to build argparse CLIs using Python type-hints. This project, argparse-tui, is integrated into Yapx with the extra `yapx[tui]`.

### [Myke](https://www.f2dv.com/code/r/myke/i/)

Myke is a simple CLI task runner, a la GNU `make`, built using `Yapx`. This project, argparse-tui, is integrated into Myke.
