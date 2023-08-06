# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cryptronics']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cryptronics',
    'version': '0.1.0',
    'description': 'Easy to use crypto API for python.',
    'long_description': None,
    'author': 'vsaverin',
    'author_email': 'vasiliy.saverin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
