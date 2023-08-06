# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pythogen', 'pythogen.parsers']

package_data = \
{'': ['*'], 'pythogen': ['templates/*', 'templates/client/*']}

install_requires = \
['inflection>=0.5.1,<0.6.0',
 'jinja2>=3.1.1,<4.0.0',
 'pyyaml>=6.0,<7.0',
 'rich>=12.2.0,<13.0.0',
 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['pythogen = pythogen.entrypoint:run']}

setup_kwargs = {
    'name': 'pythogen',
    'version': '0.0.20',
    'description': 'Generator of python HTTP-clients from OpenApi specification.',
    'long_description': '<div>\n  <p align="center">\n    <img src="docs/images/logo.png" height="100">\n  </p>\n  <h1 align="center"><strong>Pythogen</strong></h1>\n</div>\n\nGenerator of python HTTP-clients from OpenApi specification based on `httpx` and `pydantic`.\n\n[![Build Status](https://github.com/artsmolin/pythogen/actions/workflows/main.yml/badge.svg)](https://github.com/artsmolin/pythogen/actions)\n[![codecov](https://codecov.io/gh/artsmolin/pythogen/branch/main/graph/badge.svg?token=6JR6NB8Y9Z)](https://codecov.io/gh/artsmolin/pythogen)\n[![Python](https://img.shields.io/pypi/pyversions/pythogen.svg)](https://pypi.python.org/pypi/pythogen/)\n[![pypi](https://img.shields.io/pypi/v/pythogen.svg)](https://pypi.org/project/pythogen/)\n[![license](https://img.shields.io/github/license/artsmolin/pythogen.svg)](https://github.com/artsmolin/pythogen/blob/master/LICENSE)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n---\n\n<p align="center">\n  <img src="docs/images/example.png">\n</p>\n\n## Features\n- [Discriminator](/docs/discriminator.md)\n- Sync and async clients\n- Tracing\n- Metrics\n\n## Installation\n```shell\npip install pythogen\n```\n\n## Usage\n### Generate ordinary clients\n- Asynchronous client\n  ```shell\n  pythogen path/to/input/openapi.yaml path/to/output/client.py\n  ```\n- Synchronous client\n  ```shell\n  pythogen path/to/input/openapi.yaml path/to/output/client.py --sync\n  ```\n### Generate client as python-package\n```shell\npythogen path/to/input/openapi.yaml path/to/package/output --package-version=0.0.1 --package-authors="Rick, Morty"\n```\n- `--package-version` — required;\n- `--package-authors` — optional;\n- `path/to/package/output` — path to the directory where package will be saved.\n\n## Development\n- Activate environment\n    ```shell\n    rm -rf venv || true\n    python3.9 -m venv venv\n    source venv/bin/activate\n    make requirements\n    ```\n- Make changes\n- Run `make test`\n- Execute `make clients-for-tests && make test-clients`\n',
    'author': 'Artur Smolin',
    'author_email': 'artursmolin@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/artsmolin/pythogen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
