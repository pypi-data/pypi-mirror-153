import sys
from argparse import ArgumentParser
from dataclasses import dataclass
from queue import Empty
from types import SimpleNamespace
from typing import IO, Any, Callable, Dict, List, NoReturn, Optional, Tuple, Type, Union

from barim import ansi
from barim.abstracts import _DecoratedSingleton
from barim.exceptions import CommandDuplicateError
from barim.utils import spacer


@dataclass
class Argument:
    """
    Use to declare an arguments for a provided command
    """

    name: str
    description: Optional[str]


@dataclass
class Option:
    """
    Use to declare an option for a provided command
    """

    short: str
    long: str
    description: Optional[str] = None
    default: Optional[Any] = None

    required: bool = False

    append: bool = False
    count: bool = False
    extend: bool = False
    store: bool = False

    def __post_init__(self) -> None:
        super().__init__()

        if len(self.short) != 1 or not self.short.isalpha():
            raise ValueError("Short class attribute must be 1 in length and from the alphabet")

        if len(self.long) <= 1 or not self.long.isalpha():
            raise ValueError("Long class attribute must contain character from the alphabet")

        actions = [self.append, self.count, self.extend, self.store]
        if actions.count(True) > 1:
            raise ValueError("Conflicting between actions. Set only one of them to True")


@dataclass
class _GlobalOption(Option):

    action: Optional[str] = None

    def __post_init__(self) -> None:
        super().__post_init__()

        if self.action is not None and self.store is True:
            raise ValueError(
                "Unable to initialize _GlobalCommandOption if attributes action and store are set. Choose only one."
            )


class Command:
    """
    Class that should be inherited to allow the creation of commands.
    """

    name: str
    description: Optional[str] = None
    version: Optional[str] = None

    arguments: Optional[List[Argument]] = None
    options: Optional[List[Option]] = None

    def __init__(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        version: Optional[str] = None,
        arguments: Optional[List[Argument]] = None,
        options: Optional[List[Option]] = None,
        handle: Optional[Callable] = None,
    ):
        self.color = ansi.Color.CYAN

        if not hasattr(self, "name"):
            if name is None:
                raise ValueError("Attribute 'name' not provided")
            else:
                self.name = name
        if self.arguments is None:
            self.arguments = arguments if arguments is not None else []
        if self.options is None:
            self.options = options if options is not None else []
        if self.description is None:
            self.description = description or f"Add a new description {ansi.wrap(self.color, '°˖✧◝(⁰▿⁰)◜✧˖°')}"
        if self.version is None:
            self.version = version or "unknown"

        if handle is not None:
            # Patching handle function to allow creation of command in an FP friendly way
            self.handle = handle  # type: ignore[assignment]  # Too dynamic for mypy

    def __eq__(self, other):
        """Allow to create sets of command objects"""
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        """Allow to create sets of command objects"""
        return hash(self.name)

    def handle(self, argv: SimpleNamespace, opts: SimpleNamespace) -> None:
        """This method must be implemented"""
        raise NotImplementedError("Method .handle() must be implemented")


class _ArgumentParser(ArgumentParser):
    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        version: Optional[str] = None,
        arguments: Optional[List[Argument]] = None,
        options: Optional[List[Option]] = None,
        commands: Optional[List[Command]] = None,
    ) -> None:
        self.name = name
        self.color = ansi.Color.CYAN
        self.arguments = arguments or []
        self.options = options or []
        self.global_options = [
            _GlobalOption(short="h", long="help", description="Display help message", action="print_help"),
            _GlobalOption(short="V", long="version", description="Display version number", action="print_version"),
            _GlobalOption(short="v", long="verbose", description="Display more log message", count=True, default=0),
        ]
        self.description = description or f"Add a new description {ansi.wrap(self.color, '°˖✧◝(⁰▿⁰)◜✧˖°')}"
        self.version = version or "unknown"
        self.commands = commands or []

        super().__init__(description=self.description, add_help=False)

        for argument in self.arguments:
            self.add_argument(argument.name, help=argument.description)

        # Add default options
        options = self.options + self.global_options  # type: ignore[operator]  # _GlobalOption and Option share the same attributes and methods

        for option in options:
            args = [f"-{option.short}", f"--{option.long}"]
            kwargs = {"required": option.required, "action": "store_true"}

            if option.store:
                kwargs["action"] = "store"
            elif option.count:
                kwargs["action"] = "count"
            elif option.append:
                kwargs["action"] = "append"
            elif option.extend:
                kwargs["action"] = "extend"
            else:
                pass

            if option.default is not None:
                kwargs["default"] = option.default

            self.add_argument(*args, **kwargs)  # type: ignore[arg-type]  # Too dynamic for mypy

    def error(self, message: str) -> NoReturn:
        print(f"{ansi.error('Error')}: {message}")
        sys.exit(2)

    def format_help(self) -> str:
        """
        Format help message w/ the self generated context

        :return: str
        """
        help_message = f"""{ansi.wrap(ansi.Style.BOLD, '{name}')} version {ansi.wraps([ansi.Style.BOLD, ansi.Color.GREEN], '{version}')}

{ansi.wrap(ansi.Style.BOLD, 'DESCRIPTION')}
    {{description}}

{ansi.wrap(ansi.Style.BOLD, 'USAGE')}
    {{usage}}
"""

        context = self.generate_context()

        if context["arguments"]:
            help_message = f"{help_message}\n{ansi.wrap(ansi.Style.BOLD, 'ARGUMENTS')}\n\t{{arguments}}\n".expandtabs(4)

        if context["global_options"]:
            help_message = (
                f"{help_message}\n{ansi.wrap(ansi.Style.BOLD, 'GLOBAL OPTIONS')}\n\t{{global_options}}\n".expandtabs(4)
            )

        if context["options"]:
            help_message = f"{help_message}\n{ansi.wrap(ansi.Style.BOLD, 'OPTIONS')}\n\t{{options}}\n".expandtabs(4)

        if context["commands"]:
            help_message = (
                f"{help_message}\n{ansi.wrap(ansi.Style.BOLD, 'AVAILABLE COMMANDS')}\n\t{{commands}}\n".expandtabs(4)
            )

        return help_message.format(**context)

    def format_version(self) -> str:
        context = self.generate_context()
        version = f"{ansi.wrap(ansi.Style.BOLD, '{name}')} version {ansi.wraps([ansi.Style.BOLD, ansi.Color.GREEN], '{version}')}"
        return version.format(**context)

    def generate_context(self) -> Dict[str, str]:
        """
        Generate the context necessary to format help message template

        :return: Dict[str, str]
        """
        usage_args = [ansi.wrap(ansi.Style.UNDERLINE, self.name)]

        if self.arguments:
            usage_string = " ".join([f"<{argument.name}>" for argument in self.arguments])
            usage_args.append(usage_string)

        if self.options:
            usage_string = " ".join([f"[-{option.short}]" for option in self.options])
            usage_args.append(usage_string)

        usage = " ".join(usage_args)

        arguments = "\n\t".expandtabs(4).join(
            [spacer(ansi.wrap(self.color, f"<{argument.name}>"), argument.description) for argument in self.arguments]  # type: ignore[arg-type]  # Optional[str] will display None as str
        )

        global_options = "\n\t".expandtabs(4).join(
            [
                spacer(ansi.wrap(self.color, f"-{option.short}, --{option.long}"), option.description)  # type: ignore[arg-type]  # Optional[str] will display None as str
                for option in self.global_options
            ]
        )

        options = "\n\t".expandtabs(4).join(
            [
                spacer(ansi.wrap(self.color, f"-{option.short}, --{option.long}"), option.description)  # type: ignore[arg-type]  # Optional[str] will display None as str
                for option in self.options
            ]
        )

        commands = "\n\t".expandtabs(4).join(
            [spacer(ansi.wrap(self.color, command.name), command.description) for command in self.commands]  # type: ignore[arg-type]  # Optional[str] will display None as str
        )

        return {
            "name": self.name,
            "description": self.description,  # type: ignore[dict-item]  # Optional[str] will display None as str
            "version": self.version,
            "usage": usage,
            "arguments": arguments,
            "global_options": global_options,
            "options": options,
            "commands": commands,
        }

    def parse(self, args: Optional[List[str]] = None) -> Tuple[SimpleNamespace, SimpleNamespace]:
        """
        Parse args and sort them by arguments or options

        :param args: Optional[List[str]] (default sys.argv[1:])
        :return: Tuple[SimpleNamespace, SimpleNameSpace]
        """
        if args is None:
            if len(sys.argv) > 1:
                args = sys.argv[1:]
            else:
                self.error("No arguments provided")
        else:
            args = args

        for option in self.global_options:
            if (f"--{option.long}" in args or f"-{option.short}" in args) and option.action is not None:
                func = getattr(self, option.action)
                func(exit_code=0)

        argv = self.parse_args(args)

        res_argv = {argument.name: getattr(argv, argument.name) for argument in self.arguments}
        res_opts = {option.long: getattr(argv, option.long) for option in self.options + self.global_options}  # type: ignore[operator]  # _GlobalOption and Option share the same attributes and methods

        return SimpleNamespace(**res_argv), SimpleNamespace(**res_opts)

    def print_help(self, file: Optional[IO[str]] = None, exit_code: Optional[int] = None) -> None:
        print(self.format_help())
        if exit_code is not None:
            sys.exit(exit_code)

    def print_usage(self, file: Optional[IO[str]] = None) -> None:
        self.print_help()

    def print_version(self, exit_code: Optional[int] = None) -> None:
        print(self.format_version())
        if exit_code is not None:
            sys.exit(exit_code)


class Application:
    """
    Main CLI handler
    """

    def __init__(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        version: Optional[str] = None,
    ) -> None:
        self._parser: Optional[_ArgumentParser] = None

        self.color = ansi.Color.CYAN
        self.name = name or "unknown"
        self.description = description or f"Add a new description {self.color}°˖✧◝(⁰▿⁰)◜✧˖°{ansi.Style.RESET}"
        self.version = version or f"{self.color}unknown{ansi.Style.RESET}"
        self.commands: List[Command] = []

    @property
    def parser(self) -> _ArgumentParser:
        """
        Lazy loaded _ArgumentParser for main application. This property should
        only be used when application is run w/ default=True.

        :return: _ArgumentParser
        """
        if self._parser is None:
            self._parser = _ArgumentParser(
                name=self.name,
                description=self.description,
                version=self.version,
                arguments=[Argument(name="command", description="The command to run")],
                options=[],
                commands=self.commands,
            )
        return self._parser

    def match_command(self, name: str) -> Command:
        """
        Return the command corresponding to the provided name.
        Exit the program in case the command is not found.

        :param name: str
        :return: Command
        """
        for command in self.commands:
            if command.name == name:
                return command
        self.parser.error(f"Unable to find matching command '{sys.argv[1]}'")

    def register(self, command: Union[Command, Type[Command]]) -> "Application":
        """
        Register a command to make it available for application.
        This method is chainable.

        :param command: Union[Command, Type[Command]]
        :return: Application
        """
        if isinstance(command, type):
            command = command()

        self.commands.append(command)

        if len(set(self.commands)) != len(self.commands):
            raise CommandDuplicateError("Found duplicated command registered.")

        return self

    def run(self, default: bool = False) -> None:
        """
        Run the cli application

        :param default: Set to True when a single registered command must be used as default
        """
        decorated_commands = []

        while True:
            try:
                item = _DecoratedSingleton().queue.get(block=False)
            except Empty:
                break
            else:
                decorated_commands.append(item)

        self.commands.extend(decorated_commands)

        if default:
            if len(self.commands) != 1:
                raise RuntimeError("Too many command registered. Only one command must be register.")

            argv = sys.argv[1:]
            command = self.commands[0]
        else:
            argv = sys.argv[2:]
            args, _ = self.parser.parse([sys.argv[1]] if len(sys.argv) >= 2 else [])
            command = self.match_command(args.command)

        parser = _ArgumentParser(
            name=command.name,
            description=command.description,
            version=command.version,
            arguments=command.arguments,
            options=command.options,
        )

        args, opts = parser.parse(argv)
        command.handle(args, opts)
