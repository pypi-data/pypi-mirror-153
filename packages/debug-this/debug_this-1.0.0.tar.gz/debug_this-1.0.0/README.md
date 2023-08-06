# debug_this

[![Package Status][package-badge]][package-link]
[![Documentation Status][documentation-badge]][documentation-link]
[![License Status][license-badge]][license-link]
[![Build Status][build-badge]][build-link]
[![Quality Status][pre-commit-badge]][pre-commit-link]

*Python debug logging helpers*

## Installation

Using `pip`:
```bash
pip install debug_this
```

## Usage

The `debug_this` module export some decorators that can be used to debug your
fucking code:

- `@debug_this.fucking_function`
  To be used on those fucking functions that do not want to work as expected.
- `@debug_this.fucking_class`
  To be used on fucking classes that are... Well you know!

All these decorators can be used with or without arguments or keywords
arguments.

The available arguments are:

 - `logger` (`logging.Logger`, optional)
    Specify a logger instead of the default one.
 - `print_parent` (`bool`, optional)
   Print which function has called the decorated function.

## Example

```python
from __future__ import annotations

import logging

import debug_this

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

@debug_this.fucking_function(print_parent=True)
def example_function() -> None:
    logger.info("This is an example function")

@debug_this.fucking_class(logger)
class ExampleClass:
    def __init__(self) -> None:
        logger.info("This is an example class constructor")
        ExampleClass.example_static_method(self)

    def example_method(self) -> None:
        logger.info("This is an example class method")
        example_function()

    @staticmethod
    def example_static_method(cls: ExampleClass) -> None:
        logger.info("This is an example class static method")
        cls.example_method()

if __name__ == "__main__":
    ExampleClass()
```

The resulting logs should look like this:
```
DEBUG:__main__:  >>> ExampleClass.__init__
INFO:__main__:This is an example class constructor
DEBUG:__main__:    >>> ExampleClass.example_static_method
INFO:__main__:This is an example class static method
DEBUG:__main__:      >>> ExampleClass.example_method
INFO:__main__:This is an example class method
DEBUG:debug_this:        >>> example_function (parent: example_method)
INFO:__main__:This is an example function
DEBUG:debug_this:        <<< example_function
DEBUG:__main__:      <<< ExampleClass.example_method
DEBUG:__main__:    <<< ExampleClass.example_static_method
DEBUG:__main__:  <<< ExampleClass.__init__
```

[package-badge]: https://img.shields.io/pypi/v/debug-this
[package-link]: https://pypi.org/project/debug-this
[documentation-badge]: https://img.shields.io/readthedocs/python-debug-this
[documentation-link]: https://python-debug-this.readthedocs.io/en/latest
[license-badge]: https://img.shields.io/github/license/jmlemetayer/python-debug-this
[license-link]: https://github.com/jmlemetayer/python-debug-this/blob/main/LICENSE.md
[build-badge]: https://img.shields.io/github/workflow/status/jmlemetayer/python-debug-this/python-debug-this/main
[build-link]: https://github.com/jmlemetayer/python-debug-this/actions
[pre-commit-badge]: https://results.pre-commit.ci/badge/github/jmlemetayer/python-debug-this/main.svg
[pre-commit-link]: https://results.pre-commit.ci/latest/github/jmlemetayer/python-debug-this/main
