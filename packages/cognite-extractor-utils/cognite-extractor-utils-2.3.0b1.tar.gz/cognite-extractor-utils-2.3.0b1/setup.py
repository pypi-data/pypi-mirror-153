# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['cognite', 'cognite.extractorutils']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=1.0.0,<2.0.0',
 'cognite-sdk-core>=2.32.0,<3.0.0',
 'dacite>=1.6.0,<2.0.0',
 'decorator>=5.1.1,<6.0.0',
 'more-itertools>=8.12.0,<9.0.0',
 'prometheus-client>0.7.0',
 'psutil>=5.7.0,<6.0.0',
 'python-dotenv>=0.19.2,<0.20.0',
 'pyyaml>=5.3.0,<7',
 'typing-extensions>=3.7.4,<5']

setup_kwargs = {
    'name': 'cognite-extractor-utils',
    'version': '2.3.0b1',
    'description': 'Utilities for easier development of extractors for CDF',
    'long_description': '<a href="https://cognite.com/">\n    <img src="https://github.com/cognitedata/cognite-python-docs/blob/master/img/cognite_logo.png" alt="Cognite logo" title="Cognite" align="right" height="80" />\n</a>\n\nCognite Python `extractor-utils`\n================================\n[![Build Status](https://github.com/cognitedata/python-extractor-utils/workflows/release/badge.svg)](https://github.com/cognitedata/python-extractor-utils/actions)\n[![Documentation Status](https://readthedocs.com/projects/cognite-extractor-utils/badge/?version=latest&token=a9bab88214cbf624706005f6a71bbd77964efc910f8e527c7b3d75edc016397c)](https://cognite-extractor-utils.readthedocs-hosted.com/en/latest/?badge=latest)\n[![codecov](https://codecov.io/gh/cognitedata/python-extractor-utils/branch/master/graph/badge.svg?token=7AmVCpAh7I)](https://codecov.io/gh/cognitedata/python-extractor-utils)\n[![PyPI version](https://badge.fury.io/py/cognite-extractor-utils.svg)](https://pypi.org/project/cognite-extractor-utils)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cognite-extractor-utils)\n[![License](https://img.shields.io/github/license/cognitedata/python-extractor-utils)](LICENSE)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\nThe `extractor-utils` package is an extension of the Cognite Python SDK intended to simplify the development of data\nextractors or other integrations for Cognite Data Fusion.\n\nDocumentation is hosted [here](https://cognite-extractor-utils.readthedocs-hosted.com/en/latest/), including a\n[quickstart tutorial](https://cognite-extractor-utils.readthedocs-hosted.com/en/latest/quickstart.html).\n\nThe changelog is found [here](./CHANGELOG.md).\n\n## Overview\n\nThe best way to start a new extractor project is to use the `cogex` CLI. You can install that from PyPI:\n\n``` bash\npip install cognite-extractor-manager\n```\n\nTo initialize a new extractor project, run\n\n``` bash\ncogex init\n```\n\nin the directory you want your extractor project in. The `cogex` CLI will prompt you for some information about your\nproject, and then set up a poetry environment, git repository, commit hooks with type and style checks and load a\ntemplate.\n\n\n### Extensions\n\nSome source systems have a lot in common, such as RESTful APIs or systems exposing as MQTT. We therefore have extensions\nto `extractor-utils` tailroed to these protocols. These can be found in separate packages:\n\n * [REST extension](https://github.com/cognitedata/python-extractor-utils-rest)\n * [MQTT extension](https://github.com/cognitedata/python-extractor-utils-mqtt)\n\n\n## Contributing\n\nThe package is open source under the [Apache 2.0 license](./LICENSE), and contribtuions are welcome.\n\nThis project adheres to the [Contributor Covenant v2.0](https://www.contributor-covenant.org/version/2/0/code_of_conduct/)\nas a code of conduct.\n\n\n### Development environment\n\nWe use [poetry](https://python-poetry.org) to manage dependencies and to administrate virtual environments. To develop\n`extractor-utils`, follow the following steps to set up your local environment:\n\n 1. [Install poetry](https://python-poetry.org/docs/#installation) if you haven\'t already.\n\n 2. Clone repository:\n    ```\n    $ git clone git@github.com:cognitedata/python-extractor-utils.git\n    ```\n 3. Move into the newly created local repository:\n    ```\n    $ cd python-extractor-utils\n    ```\n 4. Create virtual environment and install dependencies:\n    ```\n    $ poetry install\n    ```\n\n\n### Code requirements\n\nAll code must pass [black](https://github.com/ambv/black) and [isort](https://github.com/timothycrosley/isort) style\nchecks to be merged. It is recommended to install pre-commit hooks to ensure this locally before commiting code:\n\n```\n$ poetry run pre-commit install\n```\n\nEach public method, class and module should have docstrings. Docstrings are written in the [Google\nstyle](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings). Please include unit and/or\nintegration tests for submitted code, and remember to update the [changelog](./CHANGELOG.md).\n\n',
    'author': 'Mathias Lohne',
    'author_email': 'mathias.lohne@cognite.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cognitedata/python-extractor-utils',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
