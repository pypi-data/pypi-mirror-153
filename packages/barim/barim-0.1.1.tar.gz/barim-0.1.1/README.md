# Barim

[![python](https://img.shields.io/badge/python->=3.7-blue?logo=python&logoColor=yellow)](https://python.org "Go to Python homepage")
[![pipeline - passed](https://img.shields.io/badge/pipeline-passed-brightgreen?logo=gitlab)](https://)
[![version alpha - 0.1.0](https://img.shields.io/badge/version-0.1.0-brightgreen)](https://)
[![license - MIT](https://img.shields.io/badge/license-MIT-blue)](https://)
[![code style - black](https://img.shields.io/badge/code_style-black-blue)](https://black.readthedocs.io/ "Go to Black homepage")
[![coverage - unknown](https://img.shields.io/badge/coverage-87%25-green)](https://coverage.readthedocs.io/ "Go to Coverage homepage")

Barim is a Python library that helps building CLI applications.

The [Barim API]() makes it easy to build terminal app that have one or more commands.


## Requirements

- Python ([3.7.X or later](https://www.python.org/))

## Dev requirements

- Git ([latest version](https://git-scm.com/))
- Python ([3.7.X or later](https://www.python.org/))
- Poetry ([latest version](https://python-poetry.org))

## Installing

Install with pip.

```bash
python -m pip install barim
```

Install with poetry.

```bash
poetry add barim
```

## Quickstart

This following section is dedicated to explain how barim can be used to 
create a simple CLI application. We will see how to make a terminal application 
with a default command and how we can update it to allow multiple subcommand.

### Create your first command

The first step will be to create a class that inherit from [barim.Command]() and
provide some values to the class attributes.

```python
# File name: example.py
from types import SimpleNamespace

from barim import Command


class MyCommand(Command):
    
    name = "example.py"
    description = "Print 'Hello, World!'"
    version = "0.1.0"

    def handle(self, argv: SimpleNamespace, opts: SimpleNamespace) -> None:
        print("Hello, World!")
```

Take note that the class attributes 'description' and 'version' aren't mandatory.
Only 'name' is.

> The **handle()** method **must be override** has it will be the entry point for your
software. The argv and opts parameters are two SimpleNamespace that contain
all the arguments (argv) and all the options (opts) declared in the
command class. To see how to use them check out the [Barim API]() or just continue
the quickstart guide. 

The next logical step now is just to tell barim to run the command when the
script is run. This can be done like the following.

```python
from types import SimpleNamespace

from barim import Application, Command


class MyCommand(Command):
    
    name = "my_command"
    description = "Print 'Hello, World!'"
    version = "0.1.0"

    def handle(self, argv: SimpleNamespace, opts: SimpleNamespace) -> None:
        print("Hello, World!")

        
# Notice we add a main method to be called once the script is runned        
def main() -> None:
    application = Application(name="example.py")
    application.register(MyCommand)
    application.run(default=True)


if __name__ == "__main__":
    main()
```

That should be all ! You can now test your CLI application by running the
following command.

```bash
python example.py --help
```

The output of the command should be:

```bash
example.py version 0.1.0

DESCRIPTION
    Print 'Hello, World!'

USAGE
    example.py  [-h] [-V] [-v]

GLOBAL OPTIONS
    -h (--help)             Display help message
    -V (--version)          Display version number
    -v (--verbose)          Display more log message
```

> Something to notice here is that the output doesn't show any colors (in this README) 
which will not be the case on the terminal.

### Add arguments and options to the command

Let's say now that we want to take a string as an argument to print 'Hello, {input}!'.
For this we need to declare another class variable named 'arguments' that
is a list of [barim.Argument]().

```python
from types import SimpleNamespace

from barim import Application, Argument, Command


class MyCommand(Command):
    name = "my_command"
    description = "Print 'Hello, {input}!'"
    version = "0.1.0"

    arguments = [
        Argument(
            name="input",
            description="Use input string in print statement"
        ),
    ]

    def handle(self, argv: SimpleNamespace, opts: SimpleNamespace) -> None:
        # Make use of the newly added argument
        print(f"Hello, {argv.input}")


def main() -> None:
    application = Application(name="example.py")
    application.register(MyCommand)
    application.run(default=True)


if __name__ == "__main__":
    main()
```

> Note that you can declare a [barim.Argument]() or by providing the needed data
during initialization like in the example above or by subclassing it and declaring the data as class variable.

You should now be able to run your script like the following.

```sh
python example.py Demo
```

Expected output:

```bash
Hello, Demo!
```

Now when it comes to options, it doesn't change that much. Instead of declaring
arguments you declare options and provide a list of [barim.Option]().
In our example let's say we want to turn all the letter uppercase.

```python
from types import SimpleNamespace

from barim import Application, Argument, Command, Option


class MyCommand(Command):
    name = "my_command"
    description = "Print 'Hello, {input}!'"
    version = "0.1.0"

    arguments = [
        Argument(
            name="input",
            description="Use input string in print statement"
        ),
    ]
    options = [
        Option(
            short="u",
            long="upper",
            description="Turn all the letter uppercase",
        ),
    ]

    def handle(self, argv: SimpleNamespace, opts: SimpleNamespace) -> None:
        # Make use of newly added option
        input_ = argv.input
        if opts.upper:
            input_ = input_.upper()

        print(f"Hello, {input_}")


def main() -> None:
    application = Application(name="example.py")
    application.register(MyCommand)
    application.run(default=True)


if __name__ == "__main__":
    main()
```

Now run your script as below.

```bash
python example.py demo --upper
```

Expected output:

```bash
Hello, DEMO!
```

### Create subcommands

The default parameter declare earlier in `application.run(default=True)` indicate that we only have one registered
command and that we want to use it as the default one. By removing this parameter we can now register multiple command 
to act as multiple sub command.

```python
from types import SimpleNamespace

from barim import Application, Argument, Command, Option


class MyCommand(Command):
    name = "my_command"
    description = "Print 'Hello, {input}!'"
    version = "0.1.0"

    arguments = [
        Argument(
            name="input",
            description="Use input string in print statement"
        ),
    ]
    options = [
        Option(
            short="u",
            long="upper",
            description="Turn all the letter uppercase",
        ),
    ]

    def handle(self, argv: SimpleNamespace, opts: SimpleNamespace) -> None:
        input_ = argv.input
        if opts.upper:
            input_ = input_.upper()

        print(f"Hello, {input_}")


class MyOtherCommand(Command):
    name = "my_other_command"
    description = "Print 'Hello, World!'"
    version = "0.1.0"
    
    def handle(self, argv: SimpleNamespace, opts: SimpleNamespace) -> None:
        print("Hello, World")
        
        
def main() -> None:
    application = Application(name="example.py")
    application.register(MyCommand)
    application.register(MyOtherCommand)
    application.run()


if __name__ == "__main__":
    main()
```

### Create command dynamically

As seen before, to create a command, we have to subclass [barim.Command]().
But this is not the only way we can create them. In any case you need to create them,
for example on the fly, you could do it like in the following example.

```python
from types import SimpleNamespace

from barim import Application, Command


def my_command_handle(argv: SimpleNamespace, opts: SimpleNamespace) -> None:
    print("Hello, World")

    
def main() -> None:
    my_command = Command(name="my_command", description="Print 'Hello, World!'", handle=my_command_handle)
    
    application = Application(name="example.py")
    application.register(my_command)
    application.run(default=True)

    
if __name__ == "__main__":
    main()
```

The output of the command should look like the following:

```bash
example.py version 0.1.0

DESCRIPTION
    Print 'Hello, World!'

USAGE
    example.py  [-h] [-V] [-v]

GLOBAL OPTIONS
    -h (--help)             Display help message
    -V (--version)          Display version number
    -v (--verbose)          Display more log message
```