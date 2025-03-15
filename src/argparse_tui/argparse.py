from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from contextlib import suppress
from copy import deepcopy
from typing import Any

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

        # This is specific to yapx.
        param_types: dict[str, type[Any]] | None = getattr(parser, "_dest_type", None)

        param_groups: list[tuple[int, str, argparse.Action]] = [
            (i, (x.title or "Untitled").title(), action)
            for i, x in enumerate(parser._action_groups)
            for action in x._group_actions
        ]

        for i, param_group in enumerate(param_groups):
            param_group_weight, param_group_title, param = param_group

            if (
                isinstance(param, (TuiAction, argparse._HelpAction))
                or param.help is argparse.SUPPRESS
            ):
                continue

            if isinstance(param, argparse._SubParsersAction):
                for subparser_name, subparser in param.choices.items():
                    if subparser.description != argparse.SUPPRESS and (
                        not subparser_ignorelist
                        or subparser not in subparser_ignorelist
                    ):
                        cmd_data.subcommands[CommandName(subparser_name)] = (
                            process_command(
                                CommandName(subparser_name),
                                subparser,
                                parent=cmd_data,
                            )
                        )
                continue

            param_type: type[Any] | None = param.type
            if param_types:
                param_type = param_types.get(param.dest, param.type)

            param_default_value: Any = param.default
            if param_default_value is argparse.SUPPRESS:
                param_default_value = None

            if param_type is None and param_default_value is not None:
                param_type = type(param_default_value)

            is_passthru: bool = False
            is_counting: bool = False
            is_multiple: bool = False
            is_flag: bool = False

            opts: list[str] = list(param.option_strings)
            secondary_opts: list[str] = []

            if isinstance(param, argparse._CountAction):
                is_counting = True
            elif isinstance(
                param,
                (argparse._StoreConstAction, argparse._VersionAction),
            ):
                is_flag = True
            elif type(param).__name__ == "DummyArgAction":
                # Dummy args are specific to `yapx`
                is_passthru = True
            elif (isinstance(param, argparse.BooleanOptionalAction)) or type(
                param,
            ).__name__ == "BooleanOptionalAction":
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

            if is_flag and param_type is None:
                param_type = bool

            nargs: int = (
                0
                if param.nargs in {None, argparse.SUPPRESS} and is_flag
                else 1
                if param.nargs is None or param.nargs == "?"
                else -1
                if (
                    is_passthru
                    or param.nargs
                    in {
                        "+",
                        "*",
                        argparse.REMAINDER,
                        argparse.ONE_OR_MORE,
                        argparse.ZERO_OR_MORE,
                    }
                )
                else int(param.nargs)
            )
            # Does this single parameter accept multiple values?
            # e.g., `--foo bar baz buz`
            multi_value: bool = is_passthru or nargs < 0 or nargs > 1

            # Can this parameter be specific multiple times?
            # e.g., `--foo bar --foo baz --foo buz`
            if isinstance(param, argparse._AppendAction) and nargs <= 1:
                # TODO: support 'append' action params with nargs > 1.
                is_multiple = True

            # Look for these "tags" in the help text: "secret"
            # if present, set variables and remove from the help text.
            is_secret: bool = False
            param_help: str | None = param.help
            if param_help:
                param_help = param_help.replace(
                    "%(default)s",
                    str(param_default_value),
                )
                is_secret = "<secret>" in param_help

            is_required: bool = (
                param.required
                and param_default_value is None
                and param.nargs
                not in {"?", "*", argparse.REMAINDER, argparse.ZERO_OR_MORE}
                and nargs != 0
            )

            param_value = (
                value_overrides.pop("__unknown_args__", None)
                if is_passthru
                else value_overrides.pop(param.dest, None)
            )

            if param.option_strings:
                option_data = OptionSchema(
                    name=opts,
                    type=param_type,
                    is_flag=is_flag,
                    counting=is_counting,
                    secondary_opts=secondary_opts,
                    required=is_required,
                    default=param_default_value,
                    value=param_value,
                    help=param_help,
                    choices=param.choices,
                    multiple=is_multiple,
                    multi_value=multi_value,
                    nargs=nargs,
                    secret=is_secret,
                    weight=i,
                    group_title=param_group_title,
                    group_weight=param_group_weight,
                )
                cmd_data.options.append(option_data)

            else:
                argument_data = ArgumentSchema(
                    name=param.dest,
                    type=param_type,
                    required=is_required,
                    default=param_default_value,
                    value=param_value,
                    help=param_help,
                    choices=param.choices,
                    multiple=is_multiple,
                    multi_value=multi_value,
                    nargs=nargs,
                    secret=is_secret,
                    weight=i,
                    group_title=param_group_title,
                    group_weight=param_group_weight,
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

    Creates a Textual App that presents a form-based interface for the given
    argparse parser. The TUI allows users to interactively set argument values
    through a user-friendly interface instead of command line flags.

    Args:
        parser: The argparse parser to build a TUI for
        cli_args: Arguments parsed for pre-populating the TUI form fields
        subparser_ignorelist: List of subparsers to exclude from the TUI

    Returns:
        A Textual App instance

    Examples:
    ```python
    from argparse_tui import build_tui

    import argparse
    import textual

    parser = argparse.ArgumentParser(prog="awesome-app")

    parser.add_argument("--value")

    app = build_tui(parser)

    assert isinstance(app, textual.app.App)
    ```
    """

    subcmd_args: list[str] = []
    parsed_args: dict[str, str] = {}

    if cli_args:
        # Make all args optional
        def _set_actions_optional(
            parser,
            cli_args: list[str] | None = None,
            subcmd_args: list[str] | None = None,
        ) -> list[str]:
            # Update arguments
            for action in parser._actions:
                action.required = False

            # Update subparsers
            sp_actions = parser._subparsers._actions if parser._subparsers else []
            for sp_action in sp_actions:
                sp_action.required = False
                if isinstance(sp_action, argparse._SubParsersAction):
                    found_subcmd: bool = False
                    for subcmd, subparser in sp_action.choices.items():
                        if found_subcmd:
                            _set_actions_optional(subparser)
                            continue

                        try:
                            if not cli_args:
                                raise ValueError
                            subcmd_index: int = cli_args.index(subcmd)
                        except ValueError:
                            _set_actions_optional(subparser)
                        else:
                            found_subcmd = True
                            subcmd_args.append(subcmd)
                            _set_actions_optional(
                                subparser,
                                cli_args=cli_args[(subcmd_index + 1) :],
                                subcmd_args=subcmd_args,
                            )

            return subcmd_args

        parser_copy: argparse.ArgumentParser = deepcopy(parser)
        subcmd_args = _set_actions_optional(
            parser_copy,
            cli_args=cli_args,
            subcmd_args=[],
        )

        with suppress(SystemExit):
            namespace, unknown_args = parser_copy.parse_known_args(cli_args)
            parsed_args: dict[str, str | list[str]] = vars(namespace)
            parsed_args["__unknown_args__"] = unknown_args

    schemas = introspect_argparse_parser(
        parser,
        subparser_ignorelist=subparser_ignorelist,
        value_overrides=parsed_args,
    )

    return Tui(schemas, app_name=parser.prog, subcommand_filter=subcmd_args)


def invoke_tui(
    parser: argparse.ArgumentParser,
    cli_args: Sequence[str] | None = None,
    subparser_ignorelist: list[argparse.ArgumentParser] | None = None,
) -> None:
    """Invoke a Textual UI (TUI) given an argparse parser.

    Builds and runs a TUI for the given argparse parser. This is a convenience
    function that combines build_tui() and app.run() in one call.

    Args:
        parser: The argparse parser to create a TUI for
        cli_args: Arguments parsed for pre-populating the TUI form fields
        subparser_ignorelist: List of subparsers to exclude from the TUI

    Examples:
    ```python
    import argparse
    from argparse_tui import invoke_tui

    parser = argparse.ArgumentParser(prog="awesome-app")

    parser.add_argument("--value")

    # invoke_tui(parser)
    ```
    """
    app: App = build_tui(
        parser=parser,
        cli_args=cli_args,
        subparser_ignorelist=subparser_ignorelist,
    )
    app.run()


class TuiAction(argparse.Action):
    """argparse `Action` that will analyze the parser and display a TUI.

    When this action is triggered during argument parsing, it will
    launch a Textual UI for the parser. This allows adding a '--tui'
    flag to any argparse-based CLI to provide an interactive interface.

    Args:
        option_strings: The command-line flags that trigger this action
        dest: The attribute name to store the result in
        default: The default value if the argument is not present
        help: The help text for this argument
        const: The constant value for this action
        metavar: The name to use in usage messages
        parent_parser: The parent parser if this is in a subparser

    Examples:
    ```python
    import argparse
    from argparse_tui import TuiAction

    parser = argparse.ArgumentParser()
    parser.add_argument("--tui", action=TuiAction)
    parser.print_usage()
    ```
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
    """Add a TUI argument to an existing argparse parser.

    This function adds a flag (like --tui) to the parser that, when specified,
    will launch a Textual UI for configuring the command arguments.

    Args:
        parser: The argparse parser to add the argument to
        parent_parser: The parent of the given parser, if this is a subparser
        option_strings: List of CLI flags that will invoke the TUI (default: --tui)
        help: Help text for the TUI argument
        default: Default value for the argument
        **kwargs: Additional keyword arguments passed to `parser.add_argument(...)`

    Examples:
    ```python
    import argparse
    from argparse_tui import add_tui_argument

    parser = argparse.ArgumentParser()
    add_tui_argument(parser)
    parser.print_usage()
    ```
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
    """Add a TUI subcommand to an existing argparse parser.

    This function adds a subcommand (like 'tui') to the parser that, when invoked,
    will launch a Textual UI for configuring the command arguments. This is useful
    for CLI applications that want to offer both command-line and TUI interfaces.

    Args:
        parser: The argparse parser to add the subcommand to
        command: Name of the CLI command that will invoke the TUI (default=`tui`)
        help: Help message for the subcommand
        **kwargs: If subparsers do not already exist, create with these kwargs

    Returns:
        The Argparse subparsers action that was discovered or created

    Examples:
    ```python
    import argparse
    from argparse_tui import add_tui_command

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    add_tui_command(parser)
    parser.print_usage()
    ```
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
