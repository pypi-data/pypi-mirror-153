# debug_this

[![Package Status][package-badge]][package-link]
[![Documentation Status][documentation-badge]][documentation-link]
[![License Status][license-badge]][license-link]
[![Build Status][build-badge]][build-link]
[![Quality Status][pre-commit-badge]][pre-commit-link]

*Python debug logging helpers*

## `@debug_this.function`

This decorator can be used to log the execution of a function.
```python
import logging
import debug_this

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

@debug_this.function(logger)
def example_function():
    logger.info("This is example_function")

example_function()
```

The resulting logs should look like this:
```
DEBUG:__main__:  >>> example_function
INFO:__main__:This is example_function
DEBUG:__main__:  <<< example_function
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
