# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cloudops_google']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cloudops-google',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Manuel Castillo',
    'author_email': 'manucalop@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
