# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datascience_gear']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.1',
 'numpy>=1.22.0',
 'pandas>=1.3.5',
 'scipy>=1.7.3',
 'seaborn>=0.11.2']

setup_kwargs = {
    'name': 'datascience-gear',
    'version': '0.1.6.6',
    'description': '',
    'long_description': None,
    'author': 'sinclairfr',
    'author_email': 'sixfoursuited@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
