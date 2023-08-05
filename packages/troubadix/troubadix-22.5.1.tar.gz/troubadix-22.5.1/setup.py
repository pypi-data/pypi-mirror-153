# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tests',
 'tests.helper',
 'tests.plugins',
 'tests.standalone_plugins',
 'troubadix',
 'troubadix.helper',
 'troubadix.plugins',
 'troubadix.standalone_plugins']

package_data = \
{'': ['*'],
 'tests.plugins': ['test_files/*',
                   'test_files/nasl/21.04/*',
                   'test_files/nasl/21.04/runner/*'],
 'troubadix': ['codespell/*']}

install_requires = \
['chardet>=4.0.0,<5.0.0',
 'codespell>=2.0.0,<3.0.0',
 'pontos>=22.2.1,<23.0.0',
 'python-magic>=0.4.25,<0.5.0',
 'validators>=0.18.2,<0.20.0']

entry_points = \
{'console_scripts': ['troubadix = troubadix.troubadix:main',
                     'troubadix-changed-oid = '
                     'troubadix.standalone_plugins.changed_oid:main']}

setup_kwargs = {
    'name': 'troubadix',
    'version': '22.5.1',
    'description': 'A linting and QA check tool for NASL files',
    'long_description': '![Greenbone Logo](https://www.greenbone.net/wp-content/uploads/gb_new-logo_horizontal_rgb_small.png)\n\n# Troubadix\nA linting and QA check tool for NASL files\n\n[![GitHub releases](https://img.shields.io/github/release/greenbone/troubadix.svg)](https://github.com/greenbone/troubadix/releases)\n[![PyPI release](https://img.shields.io/pypi/v/troubadix.svg)](https://pypi.org/project/troubadix/)\n[![codecov](https://codecov.io/gh/greenbone/troubadix/branch/main/graph/badge.svg?token=FFMmVmAmtb)](https://codecov.io/gh/greenbone/troubadix)\n[![Build and test](https://github.com/greenbone/troubadix/actions/workflows/ci-python.yml/badge.svg)](https://github.com/greenbone/troubadix/actions/workflows/ci-python.yml)\n\n\n## Installation\n\n### Requirements\n\nPython 3.7 and later is supported.\n\n### Install using pip\n\npip 19.0 or later is required.\n\nYou can install the latest stable release of **troubadix** from the Python\nPackage Index (pypi) using [pip]\n\n    python3 -m pip install --user troubadix\n\n### Install using poetry\n\nBecause **troubadix** is a Python application you most likely need a tool to\nhandle Python package dependencies and Python environments. Therefore we\nstrongly recommend using [pipenv] or [poetry].\n\nYou can install the latest stable release of **troubadix** and add it as\na dependency for your current project using [poetry]\n\n    poetry add troubadix\n\nFor installation via pipenv please take a look at their [documentation][pipenv].\n\n## Development\n\n**troubadix** uses [poetry] for its own dependency management and build\nprocess.\n\nFirst install poetry via pip\n\n    python3 -m pip install --user poetry\n\nAfterwards run\n\n    poetry install\n\nin the checkout directory of **troubadix** (the directory containing the\n`pyproject.toml` file) to install all dependencies including the packages only\nrequired for development.\n\nAfterwards activate the git hooks for auto-formatting and linting via\n[autohooks].\n\n    poetry run autohooks activate\n\nValidate the activated git hooks by running\n\n    poetry run autohooks check\n\n## Maintainer\n\nThis project is maintained by [Greenbone Networks GmbH][Greenbone Networks]\n\n## Contributing\n\nYour contributions are highly appreciated. Please\n[create a pull request](https://github.com/greenbone/troubadix/pulls)\non GitHub. Bigger changes need to be discussed with the development team via the\n[issues section at GitHub](https://github.com/greenbone/troubadix/issues)\nfirst.\n\n## License\n\nCopyright (C) 2021-2022 [Greenbone Networks GmbH][Greenbone Networks]\n\nLicensed under the [GNU General Public License v3.0 or later](LICENSE).\n\n[Greenbone Networks]: https://www.greenbone.net/\n[poetry]: https://python-poetry.org/\n[pip]: https://pip.pypa.io/\n[pipenv]: https://pipenv.pypa.io/\n[autohooks]: https://github.com/greenbone/autohooks\n',
    'author': 'Greenbone',
    'author_email': 'info@greenbone.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/greenbone/troubadix',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
