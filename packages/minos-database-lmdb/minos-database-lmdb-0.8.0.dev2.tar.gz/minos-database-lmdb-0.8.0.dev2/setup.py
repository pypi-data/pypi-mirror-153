# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minos',
 'minos.plugins.lmdb',
 'minos.plugins.lmdb.factories',
 'minos.plugins.lmdb.factories.saga']

package_data = \
{'': ['*']}

install_requires = \
['lmdb>=1.2.1,<2.0.0',
 'minos-microservice-common>=0.8.0.dev,<0.9.0',
 'minos-microservice-saga>=0.8.0.dev,<0.9.0']

setup_kwargs = {
    'name': 'minos-database-lmdb',
    'version': '0.8.0.dev2',
    'description': 'The lmdb plugin of the Minos Framework',
    'long_description': '<p align="center">\n  <a href="https://minos.run" target="_blank"><img src="https://raw.githubusercontent.com/minos-framework/.github/main/images/logo.png" alt="Minos logo"></a>\n</p>\n\n## minos-database-lmdb\n\n[![PyPI Latest Release](https://img.shields.io/pypi/v/minos-database-lmdb.svg)](https://pypi.org/project/minos-database-lmdb/)\n[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/minos-framework/minos-python/pages%20build%20and%20deployment?label=docs)](https://minos-framework.github.io/minos-python)\n[![License](https://img.shields.io/github/license/minos-framework/minos-python.svg)](https://github.com/minos-framework/minos-python/blob/main/LICENSE)\n[![Coverage](https://codecov.io/github/minos-framework/minos-python/coverage.svg?branch=main)](https://codecov.io/gh/minos-framework/minos-python)\n[![Stack Overflow](https://img.shields.io/badge/Stack%20Overflow-Ask%20a%20question-green)](https://stackoverflow.com/questions/tagged/minos)\n\n## Summary\n\nMinos is a framework which helps you create [reactive](https://www.reactivemanifesto.org/) microservices in Python. Internally, it leverages Event Sourcing, CQRS and a message driven architecture to fulfil the commitments of an asynchronous environment.\n\n## Installation\n\nInstall the dependency:\n\n```shell\npip install minos-database-lmdb\n```\n\nSet the database client on the `config.yml` file:\n\n```yaml\n...\ndatabases:\n  saga:\n    client: minos.plugins.lmdb.LmdbDatabaseClient\n    path: "./saga.lmdb"\n  ...\n...\n```\n\n## Documentation\n\nThe official API Reference is publicly available at the [GitHub Pages](https://minos-framework.github.io/minos-python).\n\n## Source Code\n\nThe source code of this project is hosted at the [GitHub Repository](https://github.com/minos-framework/minos-python).\n\n## Getting Help\n\nFor usage questions, the best place to go to is [StackOverflow](https://stackoverflow.com/questions/tagged/minos).\n\n## Discussion and Development\n\nMost development discussions take place over the [GitHub Issues](https://github.com/minos-framework/minos-python/issues). In addition, a [Gitter channel](https://gitter.im/minos-framework/community) is available for development-related questions.\n\n## License\n\nThis project is distributed under the [MIT](https://raw.githubusercontent.com/minos-framework/minos-python/main/LICENSE) license.\n',
    'author': 'Minos Framework Devs',
    'author_email': 'hey@minos.run',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.minos.run/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
