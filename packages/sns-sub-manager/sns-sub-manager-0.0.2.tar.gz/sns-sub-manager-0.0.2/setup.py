# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sns_sub_manager',
 'sns_sub_manager.routes',
 'sns_sub_manager.schemas',
 'sns_sub_manager.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiobotocore>=2.2.0,<3.0.0',
 'email-validator>=1.2.0,<2.0.0',
 'fastapi-health>=0.4.0,<0.5.0',
 'fastapi>=0.75.2,<0.76.0',
 'phonenumbers>=8.12.47,<9.0.0',
 'uvicorn>=0.17.6,<0.18.0']

entry_points = \
{'console_scripts': ['sns-sub-manager = sns_sub_manager.__main__:main']}

setup_kwargs = {
    'name': 'sns-sub-manager',
    'version': '0.0.2',
    'description': 'AWS SNS Subscription Manager',
    'long_description': "# AWS SNS Subscription Manager\n\n[![PyPI](https://img.shields.io/pypi/v/sns-sub-manager.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/sns-sub-manager.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/sns-sub-manager)][python version]\n[![License](https://img.shields.io/pypi/l/sns-sub-manager)][license]\n\n[![Read the documentation at https://sns-sub-manager.readthedocs.io/](https://img.shields.io/readthedocs/sns-sub-manager/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/andrewthetechie/sns-sub-manager/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/andrewthetechie/sns-sub-manager/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/sns-sub-manager/\n[status]: https://pypi.org/project/sns-sub-manager/\n[python version]: https://pypi.org/project/sns-sub-manager\n[read the docs]: https://sns-sub-manager.readthedocs.io/\n[tests]: https://github.com/andrewthetechie/sns-sub-manager/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/andrewthetechie/sns-sub-manager\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- Allows someone to subscribe and unsubscribe to sns topics via a rest api\n- Configure what SNS topics to manage via a YAML file\n- Per topic configuration of what types of subscriptions to accept\n- Able to turn off unsubscribe globally\n- No auth - that's your problem!\n- Docker image you can run easily\n\n## Requirements\n\n- TODO\n\n## Installation\n\nYou can install _AWS SNS Subscription Manager_ via [pip] from [PyPI]:\n\n```console\n$ pip install sns-sub-manager\n```\n\n## Usage\n\nYou probably don't want to be using this to be honest.\n\nSomeday, there will be info here. For today...\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_AWS SNS Subscription Manager_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/andrewthetechie/sns-sub-manager/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/andrewthetechie/sns-sub-manager/blob/main/LICENSE\n[contributor guide]: https://github.com/andrewthetechie/sns-sub-manager/blob/main/CONTRIBUTING.md\n[command-line reference]: https://sns-sub-manager.readthedocs.io/en/latest/usage.html\n",
    'author': 'Andrew Herrington',
    'author_email': 'andrew.the.techie@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andrewthetechie/sns-sub-manager',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
