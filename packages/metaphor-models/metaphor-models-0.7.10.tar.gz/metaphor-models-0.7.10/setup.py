# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['metaphor', 'metaphor.models']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'metaphor-models',
    'version': '0.7.10',
    'description': '',
    'long_description': None,
    'author': 'Metaphor',
    'author_email': 'dev@metaphor.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
