# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dotjson']

package_data = \
{'': ['*']}

install_requires = \
['flatten-json>=0.1.13,<0.2.0',
 'pydantic>=1.9.1,<2.0.0',
 'pytest-cov>=3.0.0,<4.0.0',
 'pytest-md-report>=0.2.0,<0.3.0',
 'pytest>=7.1.2,<8.0.0']

setup_kwargs = {
    'name': 'dotjson',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Aakash Khanna',
    'author_email': 'aakashkh13@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
