from __future__ import annotations

import argparse
import sys
from contextlib import suppress
from copy import deepcopy
from typing import Any, Sequence

from textual.app import App

from .constants import DEFAULT_COMMAND_NAME
from .schemas import ArgumentSchema, CommandName, CommandSchema, OptionSchema
from .tui import Tui


def introspect_argparse_parser(
    parser: argparse.ArgumentParser,
    subparser_ignorelist: list[argparse.ArgumentParser] | None = None,
    value_overrides: dict[str, Any] | None = None,
) -> dict[CommandName, CommandSchema]:
    if value_overrides is None:
        value_overrides = {}

    def process_command(
        cmd_name: CommandName,
        parser: argparse.ArgumentParser,
        parent=None,
    ) -> CommandSchema:
        cmd_data = CommandSchema(
            name=cmd_name,
            docstring=parser.description,
            options=[],
            arguments=[],
            subcommands={},
            parent=parent,
        )

        # this is specific to yapx.
        param_types: dict[str, type[Any]] | None = getattr(parser, "_dest_type", None)

        for param in parser._actions:
            if isinstance(param, TuiAction) or argparse.SUPPRESS in [
                param.help,
                param.default,
            ]:
                continue

            if isinstance(param, argparse._SubParsersAction):
                for subparser_name, subparser in param.choices.items():
                    if subparser.description != argparse.SUPPRESS and (
                        not subparser_ignorelist
                        or subparser not in subparser_ignorelist
                    ):
                        cmd_data.subcommands[
                            CommandName(subparser_name)
                        ] = process_command(
                            CommandName(subparser_name),
                            subparser,
                            parent=cmd_data,
                        )
                continue

            param_type: type[Any] | None = param.type
            if param_types:
                param_type = param_types.get(param.dest, param.type)

            if param_type is None and param.default is not None:
                param_type = type(param.default)

            is_counting: bool = False
            is_multiple: bool = False
            is_flag: bool = False

            opts: list[str] = param.option_strings
            secondary_opts: list[str] = []

            if isinstance(param, argparse._CountAction):
                is_counting = True
            elif isinstance(param, argparse._StoreConstAction):
                is_flag = True
            elif (
                sys.version_info >= (3, 9)
                and isinstance(param, argparse.BooleanOptionalAction)
            ) or type(param).__name__ == "BooleanOptionalAction":
                # check the type by name, because 'BooleanOptionalAction'
                # is often manually backported to Python versions < 3.9.
                if param_type is None:
                    param_type = bool
                is_flag = True

                if hasattr(param, "_negation_option_strings"):
                    # this is specific to `yapx`
                    secondary_opts = param._negation_option_strings
                    opts = [x for x in param.option_strings if x not in secondary_opts]
                else:
                    secondary_prefix: str = "--no-"
                    opts = [
                        x
                        for x in param.option_strings
                        if not x.startswith(secondary_prefix)
                    ]
                    secondary_opts = [x for x in param.option_strings if x not in opts]

            nargs: int = (
                0
                if param.nargs is None and is_flag
                else 1
                if param.nargs is None or param.nargs == "?"
                else -1
                if param.nargs in ["+", "*", argparse.REMAINDER]
                else int(param.nargs)
            )
            multi_value: bool = nargs < 0 or nargs > 1

            if isinstance(param, argparse._AppendAction) and nargs <= 1:
                # TODO: support 'append' action params with nargs > 1.
                is_multiple = True

            # look for these "tags" in the help text: "secret"
            # if present, set variables and remove from the help text.
            is_secret: bool = False
            param_help: str | None = param.help
            if param_help:
                param_help = param_help.replace("%(default)s", str(param.default))

                tag_prefix: str = "<"
                tag_suffix: str = ">"
                tag_start: int = param_help.find(tag_prefix)
                if tag_start >= 0:
                    tag_end: int = param_help.find(tag_suffix)
                    if tag_end > tag_start:
                        tag_txt: str = param_help[tag_start : tag_end + 1]
                        tags: list[str] = [x.strip() for x in tag_txt[1:-1].split(",")]
                        is_secret = "secret" in tags
                        if any([is_secret]):
                            param_help = param_help.replace(tag_txt, "")

            is_required: bool = (
                param.required
                and param.default is None
                and param.nargs not in ["?", "*", argparse.REMAINDER]
                and nargs != 0
            )

            if param.option_strings:
                option_data = OptionSchema(
                    name=opts,
                    type=param_type,
                    is_flag=is_flag,
                    counting=is_counting,
                    secondary_opts=secondary_opts,
                    required=is_required,
                    default=param.default,
                    value=value_overrides.get(param.dest),
                    help=param_help,
                    choices=param.choices,
                    multiple=is_multiple,
                    multi_value=multi_value,
                    nargs=nargs,
                    secret=is_secret,
                )
                cmd_data.options.append(option_data)

            else:
                argument_data = ArgumentSchema(
                    name=param.dest,
                    type=param_type,
                    required=is_required,
                    default=param.default,
                    value=value_overrides.get(param.dest),
                    help=param_help,
                    choices=param.choices,
                    multiple=is_multiple,
                    multi_value=multi_value,
                    nargs=nargs,
                    secret=is_secret,
                )
                cmd_data.arguments.append(argument_data)

        return cmd_data

    data: dict[CommandName, CommandSchema] = {}

    root_cmd_name = CommandName(parser.prog.split(".", 1)[0])

    data[root_cmd_name] = process_command(root_cmd_name, parser)

    return data


def build_tui(
    parser: argparse.ArgumentParser,
    cli_args: Sequence[str] | None = None,
    subparser_ignorelist: list[argparse.ArgumentParser] | None = None,
) -> App:
    """Build a Textual UI (TUI) given an argparse parser.

    Args:
        parser: ...
        cli_args: Arguments parsed for pre-populating the TUI form.
        subparser_ignorelist: ...

    Returns:
        a Textualize App

    Examples:
        >>> import argparse
        >>> from argparse_tui import build_tui
        >>> import textual
        ...
        >>> parser = argparse.ArgumentParser(prog="awesome-app")
        >>> _ = parser.add_argument("--value")
        ...
        >>> app = build_tui(parser)
        ...
        >>> isinstance(app, textual.app.App)
        True
    """

    cmd_filter: str | None = None
    parsed_args: dict[str, str] = {}

    if cli_args:
        for x in cli_args:
            if not x.startswith("-"):
                cmd_filter = x
                break

        # Make all args optional
        def _set_actions_optional(parser):
            # Update arguments

            for action in parser._actions:
                action.required = False

            # Update subparsers
            if parser._subparsers:
                for sp_action in parser._subparsers._actions:
                    sp_action.required = False
                    if isinstance(sp_action, argparse._SubParsersAction):
                        for subparser in sp_action.choices.values():
                            _set_actions_optional(subparser)

        parser_copy: argparse.ArgumentParser = deepcopy(parser)
        _set_actions_optional(parser_copy)

        with suppress(SystemExit):
            namespace, _unknown_args = parser_copy.parse_known_args(cli_args)
            parsed_args = vars(namespace)

    schemas = introspect_argparse_parser(
        parser,
        subparser_ignorelist=subparser_ignorelist,
        value_overrides=parsed_args,
    )

    return Tui(schemas, app_name=parser.prog, command_filter=cmd_filter)


def invoke_tui(
    parser: argparse.ArgumentParser,
    cli_args: Sequence[str] | None = None,
    subparser_ignorelist: list[argparse.ArgumentParser] | None = None,
) -> None:
    """Invoke a Textual UI (TUI) given an argparse parser.

    Args:
        parser: ...
        cli_args: Arguments parsed for pre-populating the TUI form.
        subparser_ignorelist: ...

    Examples:
        >>> import argparse
        >>> from argparse_tui import invoke_tui
        ...
        >>> parser = argparse.ArgumentParser(prog="awesome-app")
        >>> _ = parser.add_argument("--value")
        ...
        >>> invoke_tui(parser)  # doctest: +SKIP
    """
    app: App = build_tui(
        parser=parser,
        cli_args=cli_args,
        subparser_ignorelist=subparser_ignorelist,
    )
    app.run()


class TuiAction(argparse.Action):
    """argparse `Action` that will analyze the parser and display a TUI.

    Args:
        option_strings: ...
        dest: ...
        default: ...
        help: ...
        const: ...
        metavar: ...
        parent_parser: ...

    Examples:
        >>> import argparse
        >>> from argparse_tui import TuiAction
        ...
        >>> parser = argparse.ArgumentParser()
        >>> _ = parser.add_argument('--tui', action=TuiAction)
        ...
        >>> parser.print_usage()
        usage: __main__.py [-h] [--tui]
    """

    def __init__(
        self,
        option_strings: list[str],
        dest: str = argparse.SUPPRESS,
        default: Any = argparse.SUPPRESS,
        help: str | None = "Open Textual UI.",  # pylint: disable=redefined-builtin # noqa: A002
        const: str | None = None,
        metavar: str | None = None,
        parent_parser: argparse.ArgumentParser | None = None,
        **_kwargs: Any,
    ):
        super().__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            help=help,
            const=const,
            metavar=metavar,
        )
        self._parent_parser = parent_parser

    def __call__(self, parser, namespace, values, option_string=None):
        root_parser: argparse.ArgumentParser = (
            self._parent_parser if self._parent_parser else parser
        )
        subparser_ignorelist: list[argparse.ArgumentParser] = (
            [] if option_string else [parser]
        )

        cli_args: list[str] = sys.argv[1:]

        if cli_args:
            if option_string:
                with suppress(ValueError):
                    _ = cli_args.pop(cli_args.index(option_string))
            else:
                with suppress(ValueError):
                    _ = cli_args.pop(
                        cli_args.index(self.dest.lower().replace("_", "-")),
                    )

        invoke_tui(
            root_parser,
            subparser_ignorelist=subparser_ignorelist,
            cli_args=cli_args,
        )

        parser.exit()


def add_tui_argument(
    parser: argparse.ArgumentParser,
    parent_parser: argparse.ArgumentParser | None = None,
    option_strings: str | list[str] | None = None,
    help: str = "Open Textual UI.",  # pylint: disable=redefined-builtin # noqa: A002
    default=argparse.SUPPRESS,
    **kwargs,
) -> None:
    """

    Args:
        parser: the argparse parser to add the argument to.
        parent_parser: the parent of the given parser.
        option_strings: list of CLI flags that will invoke the TUI
        help: ...
        default: ...
        **kwargs: passed to `parser.add_argument(...)`

    Examples:
        >>> import argparse
        >>> from argparse_tui import add_tui_argument
        ...
        >>> parser = argparse.ArgumentParser()
        ...
        >>> add_tui_argument(parser)
        ...
        >>> parser.print_usage()
        usage: __main__.py [-h] [--tui]
    """
    if not option_strings:
        option_strings = [f"--{DEFAULT_COMMAND_NAME.replace('_', '-').lstrip('-')}"]
    elif isinstance(option_strings, str):
        option_strings = [option_strings]

    parser.add_argument(
        *option_strings,
        action=TuiAction,
        default=default,
        help=help,
        parent_parser=parent_parser,
        **kwargs,
    )


def add_tui_command(
    parser: argparse.ArgumentParser,
    command: str = DEFAULT_COMMAND_NAME,
    help: str = "Open Textual UI.",  # pylint: disable=redefined-builtin # noqa: A002
    **kwargs: Any,
) -> argparse._SubParsersAction:
    """

    Args:
        parser: the argparse parser
        command: name of the CLI command that will invoke the TUI (default=`tui`)
        help: help message for the argument
        **kwargs: if subparsers do not already exist, create with these kwargs.

    Returns:
        The Argparse subparsers action that was discovered or created.

    Examples:
        >>> import argparse
        >>> from argparse_tui import add_tui_argument
        ...
        >>> parser = argparse.ArgumentParser()
        >>> subparsers = parser.add_subparsers()
        ...
        >>> _ = add_tui_command(parser)
        ...
        >>> parser.print_usage()
        usage: __main__.py [-h] {tui} ...
    """

    subparsers: argparse._SubParsersAction
    if parser._subparsers is None:
        subparsers = parser.add_subparsers(**kwargs)
    else:
        for action in parser._actions:
            if isinstance(action, argparse._SubParsersAction):
                subparsers = action
                break

    tui_parser = subparsers.add_parser(
        command,
        description=argparse.SUPPRESS,
        help=help,
    )

    add_tui_argument(
        tui_parser,
        parent_parser=parser,
        option_strings=[command],
    )

    return subparsers
