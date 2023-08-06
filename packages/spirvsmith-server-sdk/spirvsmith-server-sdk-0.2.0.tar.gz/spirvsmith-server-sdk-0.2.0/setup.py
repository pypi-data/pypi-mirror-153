# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spirvsmith_server_sdk',
 'spirvsmith_server_sdk.api',
 'spirvsmith_server_sdk.api.default_api_endpoints',
 'spirvsmith_server_sdk.apis',
 'spirvsmith_server_sdk.model',
 'spirvsmith_server_sdk.models',
 'spirvsmith_server_sdk.test']

package_data = \
{'': ['*'], 'spirvsmith_server_sdk': ['docs/*']}

install_requires = \
['python-dateutil>=2.8.2,<3.0.0', 'urllib3>=1.26.9,<2.0.0']

setup_kwargs = {
    'name': 'spirvsmith-server-sdk',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Rayan Hatout',
    'author_email': 'rayan.hatout@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
