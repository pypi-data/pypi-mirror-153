# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['molskaten']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'molskaten',
    'version': '1.0.0',
    'description': 'A (forked) python wrapper for the skolmaten service.',
    'long_description': None,
    'author': 'granis',
    'author_email': 'granis@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/granis/skolmaten-python',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
