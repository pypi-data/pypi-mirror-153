[![](https://codecov.io/gh/nickderobertis/py-app-conf/branch/master/graph/badge.svg)](https://codecov.io/gh/nickderobertis/py-app-conf)
[![PyPI](https://img.shields.io/pypi/v/py-app-conf)](https://pypi.org/project/py-app-conf/)
![PyPI - License](https://img.shields.io/pypi/l/py-app-conf)
[![Documentation](https://img.shields.io/badge/documentation-pass-green)](https://nickderobertis.github.io/py-app-conf/)
[![Github Repo](https://img.shields.io/badge/repo-github-informational)](https://github.com/nickderobertis/py-app-conf/)


#  py-app-conf

## Overview

Strongly typed and validated configuration supporting multiple file types, dynamic instantiation, and environment variables

## Getting Started

Install `py-app-conf`:

```
pip install py-app-conf
```

A simple example:

```python
import pyappconf

# Do something with pyappconf
```

See a
[more in-depth tutorial here.](
https://nickderobertis.github.io/py-app-conf/tutorial.html
)

## Development Status

This project is currently in early-stage development. There may be
breaking changes often. While the major version is 0, minor version
upgrades will often have breaking changes.

## Developing

First ensure that you have `pipx` installed, if not, install it with `pip install pipx`.

Then clone the repo and run `npm install` and `pipenv sync`. Run `pipenv shell`
to use the virtual environment. Make your changes and then run `nox` to run formatting,
linting, and tests.

Develop documentation by running `nox -s docs` to start up a dev server.

To run tests only, run `nox -s test`. You can pass additional arguments to pytest
by adding them after `--`, e.g. `nox -s test -- -k test_something`.

## Author

Created by Nick DeRobertis. MIT License.

## Links

See the
[documentation here.](
https://nickderobertis.github.io/py-app-conf/
)
