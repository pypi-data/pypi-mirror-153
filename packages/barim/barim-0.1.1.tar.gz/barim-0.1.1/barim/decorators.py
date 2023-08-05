import functools
from typing import Callable, List, Optional

from barim.abstracts import _DecoratedSingleton
from barim.base import Argument, Command, Option


def command(
    name: str,
    description: Optional[str] = None,
    version: Optional[str] = None,
    arguments: Optional[List[Argument]] = None,
    options: Optional[List[Option]] = None,
) -> Callable:
    """
    Instantiate and register globally a new command

    :param name: str
    :param description: Optional[str] = None
    :param version: Optional[str] = None
    :param arguments: Optional[List[Argument]] = None
    :param options: Optional[List[Option]] = None
    :return: Callable
    """

    def inner(func: Callable) -> Callable:
        """"""
        instance = Command(
            name=name,
            description=description,
            version=version,
            arguments=arguments,
            options=options,
            handle=func,
        )

        _DecoratedSingleton().queue.put(instance)

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> None:
            """"""
            func(*args, **kwargs)

        return wrapper

    return inner
