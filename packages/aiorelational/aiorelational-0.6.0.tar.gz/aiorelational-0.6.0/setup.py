# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiorelational']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aiorelational',
    'version': '0.6.0',
    'description': 'Relational operators for working with Async iterators',
    'long_description': 'Async relational iterators/generators for manipulating data streams\n',
    'author': 'Willem Thiart',
    'author_email': 'himself@willemthiart.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/willemt/aiorelational',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
