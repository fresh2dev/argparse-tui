from __future__ import annotations

import os
import shlex
import sys
from contextlib import suppress
from pathlib import Path
from subprocess import run
from typing import Any, Optional
from collections.abc import Sequence
from webbrowser import open as open_url

from rich.console import Console
from rich.highlighter import ReprHighlighter
from rich.text import Text
from textual import on
from textual.app import App, AutopilotCallbackType, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.css.query import NoMatches
from textual.screen import Screen
from textual.widgets import (
    Button,
    Footer,
    Label,
    Static,
    Tree,
)
from textual.widgets.tree import TreeNode

from .detect_run_string import detect_run_string
from .schemas import CommandName, CommandSchema
from .widgets.command_info import CommandInfo
from .widgets.command_tree import CommandTree
from .widgets.form import CommandForm
from .widgets.multiple_choice import NonFocusableVerticalScroll

from importlib import metadata


class CommandBuilder(Screen[None]):
    COMPONENT_CLASSES = {"version-string", "prompt", "command-name-syntax"}

    BINDINGS = [
        Binding(key="ctrl+r", action="close_and_run", description="Run Command"),
        Binding(key="ctrl+y", action="copy_command_string", description="Copy Command"),
        Binding(
            key="ctrl+t,escape",
            action="app.focus_command_tree",
            description="Focus Command Tree",
        ),
        Binding(
            key="ctrl+o,?",
            action="app.show_command_info",
            description="Command Info",
        ),
        Binding(key="ctrl+s,i,/", action="app.focus('search')", description="Search"),
        Binding(key="f1", action="about", description="About"),
        Binding("q", "exit", show=False),
    ]

    def __init__(
        self,
        command_schemas: dict[CommandName, CommandSchema],
        app_name: str,
        app_version: str | None,
        is_grouped_cli: bool,
        name: str | None = None,
        id: str | None = None,  # pylint: disable=redefined-builtin # noqa: A002
        classes: str | None = None,
    ):
        super().__init__(name, id, classes)
        self.command_data = None
        self.command_schemas = command_schemas
        self.is_grouped_cli = is_grouped_cli

        self.app_name = app_name
        self.version = app_version

        self.highlighter = ReprHighlighter()

    def compose(self) -> ComposeResult:
        tree = CommandTree("Commands", self.command_schemas)

        title_parts = [Text(self.app_name, style="b")]
        if self.version:
            version_style = self.get_component_rich_style("version-string")
            title_parts.extend(["\n", (f"v{self.version}", version_style)])

        title = Text.assemble(*title_parts)

        sidebar = Vertical(
            Label(title, id="home-commands-label"),
            tree,
            id="home-sidebar",
        )
        if self.is_grouped_cli:
            # If the root of the click app is a Group instance, then
            #  we display the command tree to users and focus it.
            tree.focus()
        else:
            # If the click app is structured using a single command,
            #  there's no need for us to display the command tree.
            sidebar.display = False

        yield sidebar

        with Vertical(id="home-body"):
            with Horizontal(id="home-command-description-container") as vs:
                vs.can_focus = False
                yield Static(self.app_name or "", id="home-command-description")

            scrollable_body = VerticalScroll(
                Static(""),
                id="home-body-scroll",
            )
            scrollable_body.can_focus = False
            yield scrollable_body
            yield Horizontal(
                NonFocusableVerticalScroll(
                    Static("", id="home-exec-preview-static"),
                    id="home-exec-preview-container",
                ),
                # Vertical(
                #     Button.success("Close & Run", id="home-exec-button"),
                #     id="home-exec-preview-buttons",
                # ),
                id="home-exec-preview",
            )

        yield Footer()

    def action_close_and_run(self) -> None:
        self.action_copy_command_string()
        self.app.post_run_command_redacted = self.command_data.to_cli_string()
        self.app.post_run_command = self.command_data.to_cli_args()
        self.app.execute_on_exit = True
        self.app.exit()

    def action_copy_command_string(self) -> None:
        cmd: list[str] = (
            ["copy"]
            if sys.platform == "win32"
            else ["pbcopy"]
            if sys.platform == "darwin"
            else ["xclip", "-selection", "clipboard"]
            # if linux
        )

        with suppress(FileNotFoundError):
            run(
                cmd,
                input=self.app_name
                + " "
                + " ".join(
                    shlex.quote(str(x))
                    for x in self.command_data.to_cli_args(redact_secret=True)
                ),
                text=True,
                check=False,
            )

    def action_exit(self) -> None:
        self.app.exit()

    def action_about(self) -> None:
        from .widgets.about import AboutDialog

        self.app.push_screen(AboutDialog())

    async def _refresh_command_form(self, node: TreeNode[CommandSchema]) -> None:
        selected_command = node.data
        if selected_command is None:
            return

        self.selected_command_schema = selected_command
        self._update_command_description(selected_command)
        self._update_execution_string_preview()
        await self._update_form_body(node)

    @on(Tree.NodeHighlighted)
    async def selected_command_changed(
        self,
        event: Tree.NodeHighlighted[CommandSchema],
    ) -> None:
        # When we highlight a node in the CommandTree, the main body of the home page updates
        # to display a form specific to the highlighted command.
        await self._refresh_command_form(event.node)

    @on(CommandForm.Changed)
    def update_command_data(self, event: CommandForm.Changed) -> None:
        self.command_data = event.command_data
        self._update_execution_string_preview()

    def _update_command_description(self, command: CommandSchema) -> None:
        """Update the description of the command at the bottom of the sidebar
        based on the currently selected node in the command tree."""
        description_box = self.query_one("#home-command-description", Static)
        description_text = command.docstring or ""
        description_text = description_text.lstrip()
        description_text = f"[b]{command.name if self.is_grouped_cli else self.app_name}[/]\n{description_text}"
        description_box.update(description_text)

    def _update_execution_string_preview(self) -> None:
        """Update the preview box showing the command string to be executed"""
        if self.command_data is not None:
            command_name_syntax_style = self.get_component_rich_style(
                "command-name-syntax",
            )
            prefix = Text(f"{self.app_name} ", command_name_syntax_style)
            new_value = self.command_data.to_cli_string(include_root_command=False)
            highlighted_new_value = Text.assemble(prefix, self.highlighter(new_value))
            prompt_style = self.get_component_rich_style("prompt")
            preview_string = Text.assemble(("$ ", prompt_style), highlighted_new_value)
            self.query_one("#home-exec-preview-static", Static).update(preview_string)

    async def _update_form_body(self, node: TreeNode[CommandSchema]) -> None:
        # self.query_one(Pretty).update(node.data)
        parent = self.query_one("#home-body-scroll", VerticalScroll)
        for child in parent.children:
            await child.remove()

        # Process the metadata for this command and mount corresponding widgets
        command_schema = node.data
        command_form = CommandForm(
            command_schema=command_schema,
            command_schemas=self.command_schemas,
        )
        await parent.mount(command_form)
        # TODO: whatever control is focused has this text added: [2026;2$y
        # disable focus-on-launch until this issue is resolved.
        # if not self.is_grouped_cli:
        #     command_form.focus()


class Tui(App):
    CSS_PATH = Path(__file__).parent / "tui.scss"

    def __init__(
        self,
        command_schemas: dict[CommandName, CommandSchema],
        app_name: str | None,
        app_version: str | None = None,
        subcommand_filter: Sequence[str] | None = None,
    ) -> None:
        super().__init__()

        self.post_run_command: list[str] = []
        self.post_run_command_redacted: str = ""

        root_cmd_name: str = next(iter(command_schemas.keys()))

        for subcmd in subcommand_filter or []:
            matching_schema: CommandSchema | None = command_schemas[
                root_cmd_name
            ].subcommands.get(subcmd)

            if not matching_schema:
                break

            root_cmd_name = CommandName(subcmd)

            command_schemas = {root_cmd_name: matching_schema}

        self.command_schemas = command_schemas
        self.is_grouped_cli = any(v.subcommands for v in command_schemas.values())
        self.execute_on_exit = False

        self.app_name = app_name if app_name else detect_run_string()
        self.app_version = app_version

        if not self.app_version:
            with suppress(Exception):
                self.app_version = metadata.version(self.app_name)

    @classmethod
    def from_schemas(cls, *args: CommandSchema, **kwargs) -> Tui:
        if not args:
            msg = "No schemas provided."
            raise ValueError(msg)

        root_schema = args[0]

        schemas: dict[CommandName, CommandSchema] = {root_schema.name: root_schema}

        for schema in args[1:]:
            schema.parent = root_schema
            root_schema.subcommands[schema.name] = schema

        return cls(schemas, **kwargs)

    def get_default_screen(self) -> CommandBuilder:
        return CommandBuilder(
            self.command_schemas,
            app_name=self.app_name,
            app_version=self.app_version,
            is_grouped_cli=self.is_grouped_cli,
        )

    @on(Button.Pressed, "#home-exec-button")
    def on_button_pressed(self):
        self.execute_on_exit = True
        self.exit()

    def run(
        self,
        *args: Any,
        headless: bool = False,
        size: tuple[int, int] | None = None,
        auto_pilot: AutopilotCallbackType | None = None,
        **kwargs: Any,
    ) -> None:
        try:
            super().run(
                *args,
                headless=headless,
                size=size,
                auto_pilot=auto_pilot,
                **kwargs,
            )
        finally:
            if self.post_run_command:
                console = Console()
                if self.post_run_command and self.execute_on_exit:
                    console.print(
                        f"Running [b cyan]{self.app_name} {self.post_run_command_redacted}[/]",
                    )

                    split_app_name = shlex.split(self.app_name)
                    program_name = split_app_name[0]
                    arguments = [*split_app_name, *self.post_run_command]
                    # update PATH to include current working dir.
                    env: dict[str, str] = os.environ.copy()
                    env["PATH"] = os.pathsep.join([os.getcwd(), env["PATH"]])
                    os.execvpe(program_name, arguments, env)

    @on(CommandForm.Changed)
    def update_command_to_run(self, event: CommandForm.Changed):
        include_root_command = not self.is_grouped_cli
        self.post_run_command = event.command_data.to_cli_args(include_root_command)

    def action_focus_command_tree(self) -> None:
        try:
            command_tree = self.query_one(CommandTree)
        except NoMatches:
            return

        command_tree.focus()

    def action_show_command_info(self) -> None:
        command_builder = self.query_one(CommandBuilder)
        self.push_screen(CommandInfo(command_builder.selected_command_schema))

    def action_visit(self, url: str) -> None:
        """Visit the given URL, via the operating system.

        Args:
            url: The URL to visit.
        """
        open_url(url)
