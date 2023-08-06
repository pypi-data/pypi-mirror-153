[![CircleCI](https://circleci.com/gh/noosenergy/jupyterauth-neptune.svg?style=svg&circle-token=f44ebd5b7c018ad366db0b750369693974874d82)](https://circleci.com/gh/noosenergy/jupyterauth-neptune)

# Jupyterauth Neptune

Custom JupyterHub `Authenticator` subclass, to enable authentication of [Jupyter hub](https://jupyter.org/hub) via the Neptune platform.


## Installation

The python package is available from the [PyPi repository](https://pypi.org/project/jupyterauth-neptune),

```sh
pip install jupyterauth-neptune
```


## Development

On Mac OSX, make sure [poetry](https://python-poetry.org/) has been installed and pre-configured,

```sh
brew install poetry
```

This project is shipped with a Makefile, which is ready to do basic common tasks.

```shell
~$ make
help                           Display this auto-generated help message
update                         Lock and install build dependencies
clean                          Clean project from temp files / dirs
format                         Run auto-formatting linters
install                        Install build dependencies from lock file
lint                           Run python linters
test                           Run pytest with all tests
package                        Build project wheel distribution
release                        Publish wheel distribution to PyPi
```
