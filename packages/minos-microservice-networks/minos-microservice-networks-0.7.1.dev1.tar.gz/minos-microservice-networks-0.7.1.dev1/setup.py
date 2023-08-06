# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minos',
 'minos.networks',
 'minos.networks.brokers',
 'minos.networks.brokers.collections',
 'minos.networks.brokers.collections.queues',
 'minos.networks.brokers.collections.queues.database',
 'minos.networks.brokers.dispatchers',
 'minos.networks.brokers.handlers',
 'minos.networks.brokers.messages',
 'minos.networks.brokers.messages.models',
 'minos.networks.brokers.publishers',
 'minos.networks.brokers.publishers.queued',
 'minos.networks.brokers.publishers.queued.queues',
 'minos.networks.brokers.subscribers',
 'minos.networks.brokers.subscribers.filtered',
 'minos.networks.brokers.subscribers.filtered.validators',
 'minos.networks.brokers.subscribers.filtered.validators.duplicates',
 'minos.networks.brokers.subscribers.filtered.validators.duplicates.database',
 'minos.networks.brokers.subscribers.queued',
 'minos.networks.brokers.subscribers.queued.queues',
 'minos.networks.brokers.subscribers.queued.queues.database',
 'minos.networks.decorators',
 'minos.networks.decorators.callables',
 'minos.networks.decorators.definitions',
 'minos.networks.decorators.definitions.http',
 'minos.networks.discovery',
 'minos.networks.discovery.clients',
 'minos.networks.http',
 'minos.networks.requests',
 'minos.networks.scheduling',
 'minos.networks.specs',
 'minos.networks.system',
 'minos.networks.testing',
 'minos.networks.testing.brokers',
 'minos.networks.testing.brokers.collections',
 'minos.networks.testing.brokers.publishers',
 'minos.networks.testing.brokers.subscribers']

package_data = \
{'': ['*']}

install_requires = \
['crontab>=0.23.0,<0.24.0', 'minos-microservice-common>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'minos-microservice-networks',
    'version': '0.7.1.dev1',
    'description': 'The networks core of the Minos Framework',
    'long_description': '<p align="center">\n  <a href="https://minos.run" target="_blank"><img src="https://raw.githubusercontent.com/minos-framework/.github/main/images/logo.png" alt="Minos logo"></a>\n</p>\n\n## minos-microservice-networks\n\n[![PyPI Latest Release](https://img.shields.io/pypi/v/minos-microservice-networks.svg)](https://pypi.org/project/minos-microservice-networks/)\n[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/minos-framework/minos-python/pages%20build%20and%20deployment?label=docs)](https://minos-framework.github.io/minos-python)\n[![License](https://img.shields.io/github/license/minos-framework/minos-python.svg)](https://github.com/minos-framework/minos-python/blob/main/LICENSE)\n[![Coverage](https://codecov.io/github/minos-framework/minos-python/coverage.svg?branch=main)](https://codecov.io/gh/minos-framework/minos-python)\n[![Stack Overflow](https://img.shields.io/badge/Stack%20Overflow-Ask%20a%20question-green)](https://stackoverflow.com/questions/tagged/minos)\n\n## Summary\n\nMinos is a framework which helps you create [reactive](https://www.reactivemanifesto.org/) microservices in Python.\nInternally, it leverages Event Sourcing, CQRS and a message driven architecture to fulfil the commitments of an\nasynchronous environment.\n\n## Documentation\n\nThe official API Reference is publicly available at the [GitHub Pages](https://minos-framework.github.io/minos-python).\n\n## Source Code\n\nThe source code of this project is hosted at the [GitHub Repository](https://github.com/minos-framework/minos-python).\n\n## Getting Help\n\nFor usage questions, the best place to go to is [StackOverflow](https://stackoverflow.com/questions/tagged/minos).\n\n## Discussion and Development\nMost development discussions take place over the [GitHub Issues](https://github.com/minos-framework/minos-python/issues). In addition, a [Gitter channel](https://gitter.im/minos-framework/community) is available for development-related questions.\n\n## License\n\nThis project is distributed under the [MIT](https://raw.githubusercontent.com/minos-framework/minos-python/main/LICENSE) license.\n',
    'author': 'Minos Framework Devs',
    'author_email': 'hey@minos.run',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.minos.run',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
