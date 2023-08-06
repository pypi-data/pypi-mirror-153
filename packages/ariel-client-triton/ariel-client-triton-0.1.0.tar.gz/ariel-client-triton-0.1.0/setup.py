# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ariel']

package_data = \
{'': ['*']}

install_requires = \
['grpcio>=1.41.0,<1.42.0', 'tritonclient[all]>=2.22.0,<3.0.0']

setup_kwargs = {
    'name': 'ariel-client-triton',
    'version': '0.1.0',
    'description': 'Client utilities for the triton inference server',
    'long_description': None,
    'author': 'Luis Vega',
    'author_email': 'vegaluisjose@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
