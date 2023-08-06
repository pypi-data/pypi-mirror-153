# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wsrouter']

package_data = \
{'': ['*']}

install_requires = \
['boltons>=21.0.0,<22.0.0',
 'orjson>=3.7.1,<4.0.0',
 'shortuuid>=1.0.9,<2.0.0',
 'starlette>=0.20.1,<0.21.0']

setup_kwargs = {
    'name': 'wsrouter',
    'version': '0.1.0',
    'description': 'Starlette Shared WebSocket Endpoint',
    'long_description': None,
    'author': 'David Morris',
    'author_email': 'gypsysoftware+gitlab@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
