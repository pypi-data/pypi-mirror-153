# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiogram_declarative', 'aiogram_declarative.abc', 'aiogram_declarative.src']

package_data = \
{'': ['*']}

install_requires = \
['aiogram>=3.0.0b2,<4.0.0', 'aiogram_dialog>=2.0.0b2,<3.0.0']

setup_kwargs = {
    'name': 'aiogram-declarative',
    'version': '0.1.7',
    'description': 'Another way to struct your telegram bots via Aiogram3',
    'long_description': None,
    'author': 'Aleks',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
