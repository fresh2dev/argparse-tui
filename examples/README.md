# Example TUI Apps

To run the example TUI apps, first clone this repo and install the requirements:

```sh
git clone https://github.com/fresh2dev/argparse-tui.git

cd argparse-tui/examples

pip install requirements.txt
```

Demos:

<!-- TOC GFM -->

- [Argparse](#argparse)
- [Argparse (Invoke)](#argparse-invoke)
- [Yapx](#yapx)
- [Myke](#myke)
- [Plain o' `sys.argv`](#plain-o-sysargv)

<!-- /TOC -->

## Argparse

```sh
./demo_argparse.py --tui
# OR, as a command:
./demo_argparse.py tui
```

## Argparse (Invoke)

```sh
./demo_argparse_invoke.py
```

## Yapx

```sh
./demo_yapx.py --tui
```

## Myke

```sh
myke --tui --myke-file ./demo_myke.py
```

## Plain o' `sys.argv`

```sh
./demo_argv.py tui
```
