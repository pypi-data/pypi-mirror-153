# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiorelational']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aiorelational',
    'version': '0.5.0',
    'description': '',
    'long_description': None,
    'author': 'Willem Thiart',
    'author_email': 'himself@willemthiart.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
