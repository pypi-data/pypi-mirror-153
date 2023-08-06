# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iceportal']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23,<1']

setup_kwargs = {
    'name': 'iceportal',
    'version': '1.1.1',
    'description': 'Python client for getting data from the ICE Portal',
    'long_description': None,
    'author': 'Fabian Affolter',
    'author_email': 'mail@fabian-affolter.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
