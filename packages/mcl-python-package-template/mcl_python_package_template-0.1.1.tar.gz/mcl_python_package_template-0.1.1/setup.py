# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mcl_python_package_template']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mcl-python-package-template',
    'version': '0.1.1',
    'description': 'The mcl_python_package_template package',
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
