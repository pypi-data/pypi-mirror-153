# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minos',
 'minos.common',
 'minos.common.config',
 'minos.common.database',
 'minos.common.database.clients',
 'minos.common.database.locks',
 'minos.common.injections',
 'minos.common.model',
 'minos.common.model.dynamic',
 'minos.common.model.serializers',
 'minos.common.model.serializers.avro',
 'minos.common.model.serializers.avro.data',
 'minos.common.model.serializers.avro.schema',
 'minos.common.model.types',
 'minos.common.protocol',
 'minos.common.protocol.avro',
 'minos.common.testing',
 'minos.common.testing.database',
 'minos.common.testing.database.factories']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<7.0.0',
 'aiomisc>=14.0.3,<15.8.0',
 'cached-property>=1.5.2,<2.0.0',
 'dependency-injector>=4.32.2,<5.0.0',
 'fastavro>=1.4.0,<2.0.0',
 'orjson>=3.5.2,<4.0.0',
 'uvloop>=0.16.0,<0.17.0']

setup_kwargs = {
    'name': 'minos-microservice-common',
    'version': '0.7.1.dev1',
    'description': 'The common core of the Minos Framework',
    'long_description': '<p align="center">\n  <a href="https://minos.run" target="_blank"><img src="https://raw.githubusercontent.com/minos-framework/.github/main/images/logo.png" alt="Minos logo"></a>\n</p>\n\n## minos-microservice-common\n\n[![PyPI Latest Release](https://img.shields.io/pypi/v/minos-microservice-common.svg)](https://pypi.org/project/minos-microservice-common/)\n[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/minos-framework/minos-python/pages%20build%20and%20deployment?label=docs)](https://minos-framework.github.io/minos-python)\n[![License](https://img.shields.io/github/license/minos-framework/minos-python.svg)](https://github.com/minos-framework/minos-python/blob/main/LICENSE)\n[![Coverage](https://codecov.io/github/minos-framework/minos-python/coverage.svg?branch=main)](https://codecov.io/gh/minos-framework/minos-python)\n[![Stack Overflow](https://img.shields.io/badge/Stack%20Overflow-Ask%20a%20question-green)](https://stackoverflow.com/questions/tagged/minos)\n\n## Summary\n\nMinos is a framework which helps you create [reactive](https://www.reactivemanifesto.org/) microservices in Python.\nInternally, it leverages Event Sourcing, CQRS and a message driven architecture to fulfil the commitments of an\nasynchronous environment.\n\n## Documentation\n\nThe official API Reference is publicly available at the [GitHub Pages](https://minos-framework.github.io/minos-python).\n\n## Source Code\n\nThe source code of this project is hosted at the [GitHub Repository](https://github.com/minos-framework/minos-python).\n\n## Getting Help\n\nFor usage questions, the best place to go to is [StackOverflow](https://stackoverflow.com/questions/tagged/minos).\n\n## Discussion and Development\nMost development discussions take place over the [GitHub Issues](https://github.com/minos-framework/minos-python/issues). In addition, a [Gitter channel](https://gitter.im/minos-framework/community) is available for development-related questions.\n\n## License\n\nThis project is distributed under the [MIT](https://raw.githubusercontent.com/minos-framework/minos-python/main/LICENSE) license.\n',
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
