# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jupyterauth_neptune']

package_data = \
{'': ['*']}

install_requires = \
['jupyterhub>=0.8', 'noos-pyk', 'tornado', 'traitlets']

setup_kwargs = {
    'name': 'jupyterauth-neptune',
    'version': '0.2',
    'description': 'Custom JupyterHub authenticator for the Neptune platform.',
    'long_description': '[![CircleCI](https://circleci.com/gh/noosenergy/jupyterauth-neptune.svg?style=svg&circle-token=f44ebd5b7c018ad366db0b750369693974874d82)](https://circleci.com/gh/noosenergy/jupyterauth-neptune)\n\n# Jupyterauth Neptune\n\nCustom JupyterHub `Authenticator` subclass, to enable authentication of [Jupyter hub](https://jupyter.org/hub) via the Neptune platform.\n\n\n## Installation\n\nThe python package is available from the [PyPi repository](https://pypi.org/project/jupyterauth-neptune),\n\n```sh\npip install jupyterauth-neptune\n```\n\n\n## Development\n\nOn Mac OSX, make sure [poetry](https://python-poetry.org/) has been installed and pre-configured,\n\n```sh\nbrew install poetry\n```\n\nThis project is shipped with a Makefile, which is ready to do basic common tasks.\n\n```shell\n~$ make\nhelp                           Display this auto-generated help message\nupdate                         Lock and install build dependencies\nclean                          Clean project from temp files / dirs\nformat                         Run auto-formatting linters\ninstall                        Install build dependencies from lock file\nlint                           Run python linters\ntest                           Run pytest with all tests\npackage                        Build project wheel distribution\nrelease                        Publish wheel distribution to PyPi\n```\n',
    'author': 'Noos Energy',
    'author_email': 'contact@noos.energy',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/noosenergy/jupyterauth-neptune',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
