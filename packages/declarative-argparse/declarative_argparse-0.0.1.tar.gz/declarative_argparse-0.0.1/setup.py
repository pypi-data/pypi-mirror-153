# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['declarative_argparse', 'declarative_argparse.options']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'declarative-argparse',
    'version': '0.0.1',
    'description': 'A simple wrapper around argparse to permit declarative construction and argument retrieval.',
    'long_description': None,
    'author': 'Rob Nelson',
    'author_email': 'nexisentertainment@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
