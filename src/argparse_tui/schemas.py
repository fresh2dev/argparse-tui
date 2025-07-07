from __future__ import annotations

import uuid
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from functools import partial
from typing import Any, NewType

from textual.content import Content


def generate_unique_id():
    return f"id_{str(uuid.uuid4())[:8]}"


@dataclass
class MultiValueParamData:
    values: list[tuple[int | float | str]]

    @staticmethod
    def process_cli_option(value) -> MultiValueParamData:
        if value is None:
            value = MultiValueParamData([])
        elif isinstance(value, tuple):
            value = MultiValueParamData([value])
        elif isinstance(value, list):
            processed_list = [
                (item,) if not isinstance(item, tuple) else item for item in value
            ]
            value = MultiValueParamData(processed_list)
        else:
            value = MultiValueParamData([(value,)])

        return value


@dataclass
class ChoiceSchema:
    # this is used in place of click.Choice
    choices: Sequence[str]

    def __post_init__(self):
        self.__name__ = "choice"


@dataclass
class ArgumentSchema:
    name: str | list[str]
    type: type[Any] | Sequence[type[Any]] | None = None
    required: bool = False
    help: Content.ContentType | None = None
    key: str | tuple[str] = field(default_factory=generate_unique_id)
    default: MultiValueParamData | Any | None = None
    value: MultiValueParamData | Any | None = None
    choices: Iterable[str] | None = None
    multiple: bool = False
    multi_value: bool = False
    nargs: int = 1
    secret: bool = False
    read_only: bool = False
    placeholder: str = ""
    weight: int = 0
    group_title: str = "Arguments"
    group_weight: int = 0

    def __post_init__(self):
        if self.help and isinstance(self.help, str):
            self.help = Content.from_markup("$text", text=self.help)

        if not isinstance(self.default, MultiValueParamData):
            self.default = MultiValueParamData.process_cli_option(self.default)

        if self.value is None:
            self.value = self.default
        elif not isinstance(self.value, MultiValueParamData):
            self.value = MultiValueParamData.process_cli_option(self.value)

        default_type: list[type[Any]] = [str]

        if not self.type:
            self.type = default_type
        elif isinstance(self.type, partial):
            # if this is an instance of `functools.partial`,
            # iterate over the args/kwargs looking for a type.
            # if not found, default to `str`.
            for x in self.type.args:
                if isinstance(x, type):
                    self.type = [x]
                    break
            else:
                for v in self.type.keywords.values():
                    if isinstance(v, type):
                        self.type = [v]
                        break
                else:
                    self.type = default_type
        elif isinstance(self.type, type) or callable(self.type):
            self.type = [self.type]
        elif len(self.type) == 1 and isinstance(self.type[0], ChoiceSchema):
            # if there is only one type and it is a 'ChoiceSchema':
            self.choices = self.type[0].choices
            self.type = default_type

        if self.choices:
            self.choices = [str(x) for x in self.choices]


@dataclass
class OptionSchema(ArgumentSchema):
    is_flag: bool = False
    counting: bool = False
    secondary_opts: list[str] | None = None
    group_title: str = "Options"
    group_weight: int = 1


@dataclass
class CommandSchema:
    name: CommandName
    docstring: Content.ContentType | None = None
    key: str = field(default_factory=generate_unique_id)
    options: list[OptionSchema] = field(default_factory=list)
    arguments: list[ArgumentSchema] = field(default_factory=list)
    subcommands: dict[CommandName, CommandSchema] = field(default_factory=dict)
    parent: CommandSchema | None = None

    def __post_init__(self) -> None:
        if self.docstring and isinstance(self.docstring, str):
            self.docstring = Content.from_markup("$text", text=self.docstring)

    @property
    def path_from_root(self) -> list[CommandSchema]:
        node = self
        path = [self]
        while True:
            node = node.parent
            if node is None:
                break
            path.append(node)
        return list(reversed(path))


CommandName = NewType("CommandName", str)
