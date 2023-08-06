"""Python debug logging helpers."""
from __future__ import annotations

import functools
import inspect
import logging
from typing import Any
from typing import Callable

module_logger = logging.getLogger(__name__)

__version__ = "1.0.2"


def fucking_function(*args_d: Any, **kwargs_d: Any) -> Any:
    """Log the execution of an unfriendly function.

    Parameters
    ----------
    logger: logging.Logger, optional
        Specify a logger instead of the default one.
    print_parent: bool, optional
        Print which function has called the decorated function.

    Examples
    --------
    >>> import logging
    >>> import debug_this
    >>>
    >>> logging.basicConfig(level=logging.DEBUG)
    >>>
    >>> logger = logging.getLogger(__name__)
    >>>
    >>> @debug_this.fucking_function(logger)
    >>> def example_function():
    ...     logger.info("This is an example function")
    >>>
    >>> example_function()
    DEBUG:__main__:  >>> example_function
    INFO:__main__:This is an example function
    DEBUG:__main__:  <<< example_function
    """
    logger: logging.Logger | None = kwargs_d.get("logger", None)
    print_parent: bool | None = kwargs_d.get("print_parent", None)

    if len(args_d) >= 1 and isinstance(args_d[0], logging.Logger):
        logger = args_d[0]

    if len(args_d) >= 2 and isinstance(args_d[1], bool):
        print_parent = args_d[1]

    if logger is None:
        logger = module_logger

    def fucking_function_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        if not inspect.isfunction(func):
            raise TypeError("This decorator must be used on a function")

        @functools.wraps(func)
        def debug_this_fucking_function(*args_f: Any, **kwargs_f: Any) -> Any:
            stack = [
                x.function
                for x in inspect.stack()
                if x[3] != "debug_this_fucking_function"
            ]
            stack_level = len(stack)
            prefix = "  " * stack_level

            assert isinstance(logger, logging.Logger)  # makes mypy happy

            if print_parent is True:
                logger.debug(f"{prefix}>>> {func.__qualname__} (parent: {stack[0]})")
            else:
                logger.debug(f"{prefix}>>> {func.__qualname__}")

            value = func(*args_f, **kwargs_f)

            logger.debug(f"{prefix}<<< {func.__qualname__}")

            return value

        return debug_this_fucking_function

    if len(args_d) == 1 and callable(args_d[0]):
        return fucking_function_decorator(args_d[0])
    else:
        return fucking_function_decorator


def fucking_class(*args_d: Any, **kwargs_d: Any) -> Any:
    """Log the execution of an unfriendly class.

    This decorator configures the :obj:`fucking_function` decorator on each
    method of the specified class. All available parameters for the
    :obj:`fucking_function` decorator can be used.

    See Also
    --------
    fucking_function

    Examples
    --------
    >>> import logging
    >>> import debug_this
    >>>
    >>> logging.basicConfig(level=logging.DEBUG)
    >>>
    >>> logger = logging.getLogger(__name__)
    >>>
    >>> @debug_this.fucking_class(logger)
    >>> class ExampleClass:
    ...     def __init__(self):
    ...         logger.info("Example constructor")
    ...
    ...     def example_method(self):
    ...         logger.info("Example method")
    >>>
    >>> e = ExampleClass()
    >>> e.example_method()
    DEBUG:__main__:  >>> ExampleClass.__init__
    INFO:__main__:Example constructor
    DEBUG:__main__:  <<< ExampleClass.__init__
    DEBUG:__main__:  >>> ExampleClass.example_method
    INFO:__main__:Example method
    DEBUG:__main__:  <<< ExampleClass.example_method
    """

    def fucking_class_decorator(cls: type) -> type:
        if not inspect.isclass(cls):
            raise TypeError("This decorator must be used on a class")

        for name, method in inspect.getmembers(cls, inspect.isfunction):
            setattr(cls, name, fucking_function(*args_d, **kwargs_d)(method))

        return cls

    if len(args_d) == 1 and callable(args_d[0]):
        cls = args_d[0]
        args_d = args_d[1:]
        return fucking_class_decorator(cls)
    else:
        return fucking_class_decorator
