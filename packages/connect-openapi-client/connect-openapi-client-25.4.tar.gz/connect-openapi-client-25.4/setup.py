# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cnct',
 'connect',
 'connect.client',
 'connect.client.contrib',
 'connect.client.contrib.locust',
 'connect.client.models',
 'connect.client.rql']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1',
 'asgiref>=3.3.4,<4.0.0',
 'connect-markdown-renderer>=2,<3',
 'httpx>=0.23',
 'inflect>=4.1',
 'requests>=2.23']

setup_kwargs = {
    'name': 'connect-openapi-client',
    'version': '25.4',
    'description': 'Connect Python OpenAPI Client',
    'long_description': '# Connect Python OpenAPI Client\n\n![pyversions](https://img.shields.io/pypi/pyversions/connect-openapi-client.svg) [![PyPi Status](https://img.shields.io/pypi/v/connect-openapi-client.svg)](https://pypi.org/project/connect-openapi-client/) [![Build Status](https://github.com/cloudblue/connect-python-openapi-client/workflows/Build%20Connect%20Python%20OpenAPI%20Client/badge.svg)](https://github.com/cloudblue/connect-python-openapi-client/actions) [![codecov](https://codecov.io/gh/cloudblue/connect-python-openapi-client/branch/master/graph/badge.svg)](https://codecov.io/gh/cloudblue/connect-python-openapi-client) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=connect-open-api-client&metric=alert_status)](https://sonarcloud.io/dashboard?id=connect-open-api-client)\n\n\n\n\n## Introduction\n\n`Connect Python OpenAPI Client` is the simple, concise, powerful and REPL-friendly CloudBlue Connect API client.\n\nIt has been designed following the [fluent interface design pattern](https://en.wikipedia.org/wiki/Fluent_interface).\n\nDue to its REPL-friendly nature, using the CloudBlue Connect OpenAPI specifications it allows developers to learn and\nplay with the CloudBlue Connect API using a python REPL like [jupyter](https://jupyter.org/) or [ipython](https://ipython.org/).\n\n\n## Install\n\n`Connect Python OpenAPI Client` requires python 3.7 or later.\n\n\n`Connect Python OpenAPI Client` can be installed from [pypi.org](https://pypi.org/project/connect-openapi-client/) using pip:\n\n```\n$ pip install connect-openapi-client\n```\n\n\n## Documentation\n\n[`Connect Python OpenAPI Client` documentation](https://connect-openapi-client.readthedocs.io/en/latest/) is hosted on the _Read the Docs_ service.\n\n\n## License\n\n``Connect Python OpenAPI Client`` is released under the [Apache License Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).\n',
    'author': 'CloudBlue',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://connect.cloudblue.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
