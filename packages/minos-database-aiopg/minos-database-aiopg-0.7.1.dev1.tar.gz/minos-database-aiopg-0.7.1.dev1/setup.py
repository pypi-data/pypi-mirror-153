# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minos',
 'minos.plugins.aiopg',
 'minos.plugins.aiopg.factories',
 'minos.plugins.aiopg.factories.aggregate',
 'minos.plugins.aiopg.factories.aggregate.snapshots',
 'minos.plugins.aiopg.factories.common',
 'minos.plugins.aiopg.factories.networks',
 'minos.plugins.aiopg.factories.networks.collections',
 'minos.plugins.aiopg.factories.networks.publishers',
 'minos.plugins.aiopg.factories.networks.subscribers']

package_data = \
{'': ['*']}

install_requires = \
['aiopg>=1.2.1,<2.0.0',
 'minos-microservice-aggregate>=0.7.0,<0.8.0',
 'minos-microservice-common>=0.7.0,<0.8.0',
 'minos-microservice-networks>=0.7.0,<0.8.0',
 'psycopg2-binary>=2.9.3,<3.0.0']

setup_kwargs = {
    'name': 'minos-database-aiopg',
    'version': '0.7.1.dev1',
    'description': 'The aiopg plugin of the Minos Framework',
    'long_description': '<p align="center">\n  <a href="https://minos.run" target="_blank"><img src="https://raw.githubusercontent.com/minos-framework/.github/main/images/logo.png" alt="Minos logo"></a>\n</p>\n\n## minos-database-aiopg\n\n[![PyPI Latest Release](https://img.shields.io/pypi/v/minos-database-aiopg.svg)](https://pypi.org/project/minos-database-aiopg/)\n[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/minos-framework/minos-python/pages%20build%20and%20deployment?label=docs)](https://minos-framework.github.io/minos-python)\n[![License](https://img.shields.io/github/license/minos-framework/minos-python.svg)](https://github.com/minos-framework/minos-python/blob/main/LICENSE)\n[![Coverage](https://codecov.io/github/minos-framework/minos-python/coverage.svg?branch=main)](https://codecov.io/gh/minos-framework/minos-python)\n[![Stack Overflow](https://img.shields.io/badge/Stack%20Overflow-Ask%20a%20question-green)](https://stackoverflow.com/questions/tagged/minos)\n\n## Summary\n\nMinos is a framework which helps you create [reactive](https://www.reactivemanifesto.org/) microservices in Python. Internally, it leverages Event Sourcing, CQRS and a message driven architecture to fulfil the commitments of an asynchronous environment.\n\n## Installation\n\nInstall the dependency:\n\n```shell\npip install minos-database-aiopg\n```\n\nSet the database client on the `config.yml` file:\n\n```yaml\n...\ndatabases:\n  default:\n    client: minos.plugins.aiopg.AiopgDatabaseClient\n    database: order_db\n    user: minos\n    password: min0s\n    host: localhost\n    port: 5432\n  query:\n    client: minos.plugins.aiopg.AiopgDatabaseClient\n    database: order_query_db\n    user: minos\n    password: min0s\n    host: localhost\n    port: 5432\n  ...\n...\n```\n\n## Documentation\n\nThe official API Reference is publicly available at the [GitHub Pages](https://minos-framework.github.io/minos-python).\n\n## Source Code\n\nThe source code of this project is hosted at the [GitHub Repository](https://github.com/minos-framework/minos-python).\n\n## Getting Help\n\nFor usage questions, the best place to go to is [StackOverflow](https://stackoverflow.com/questions/tagged/minos).\n\n## Discussion and Development\n\nMost development discussions take place over the [GitHub Issues](https://github.com/minos-framework/minos-python/issues). In addition, a [Gitter channel](https://gitter.im/minos-framework/community) is available for development-related questions.\n\n## License\n\nThis project is distributed under the [MIT](https://raw.githubusercontent.com/minos-framework/minos-python/main/LICENSE) license.\n',
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
