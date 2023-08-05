from queue import Queue
from threading import Lock
from typing import Any, Dict


class __Singleton(type):
    """
    A metaclass for singleton purpose. Every singleton class should inherit from this class by 'metaclass=__Singleton'.
    This singleton metaclass is thread safe.
    """

    __instances: Dict[Any, Any] = {}
    __lock = Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            with cls.__lock:
                if cls not in cls.__instances:
                    cls.__instances[cls] = super().__call__(*args, **kwargs)
        return cls.__instances[cls]


class _DecoratedSingleton(metaclass=__Singleton):
    """
    A singleton class that can be used to store data when using decorators
    """

    queue: Queue = Queue()
