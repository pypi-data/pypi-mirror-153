# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_injector']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.70.0', 'injector>=0.19.0']

setup_kwargs = {
    'name': 'fastapi-injector',
    'version': '0.2.0',
    'description': 'python-injector integration for FastAPI',
    'long_description': None,
    'author': 'Matyas Richter',
    'author_email': 'matyas@mrichter.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/matyasrichter/fastapi-injector',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
