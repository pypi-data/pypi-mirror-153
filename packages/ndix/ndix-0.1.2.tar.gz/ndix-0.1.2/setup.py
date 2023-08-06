# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ndix', 'ndix.src']

package_data = \
{'': ['*'], 'ndix': ['.ipynb_checkpoints/*']}

setup_kwargs = {
    'name': 'ndix',
    'version': '0.1.2',
    'description': '',
    'long_description': "# ndix ✨ \n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ndix)\n![PyPI](https://img.shields.io/pypi/v/ndix)\n\nA lightweight solution for **nested dictionaries** that are both \n- arbitrarily *deep*, \n- while having a *pretty* representation.\n\nUsage:  \n\n```$ pip install ndix``` ( or ```$ poetry add ndix``` ) \n\n\nInitialize nested dict:  \n```python\nfrom ndix import Dict\nd = Dict.nest()\n\n# Populate dict with arbitrary nesting:  \nd['first']['second']['third']['fourth']['fifth'] = 100 \n\n# check d:\nd \n>>> {'first': {'second': {'third': {'fourth': {'fifth': 100}}}}}\n```\n\n\n\n\n\n\n",
    'author': 'Michael Moor',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mi92/ndix',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
