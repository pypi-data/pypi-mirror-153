# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['microdata_validator']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema>=4.2.1,<5.0.0']

setup_kwargs = {
    'name': 'microdata-validator',
    'version': '2.0.0',
    'description': 'Python package for validating datasets in the microdata platform',
    'long_description': None,
    'author': 'microdata-developers',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
