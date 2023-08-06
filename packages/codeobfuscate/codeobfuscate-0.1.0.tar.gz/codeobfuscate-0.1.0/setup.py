# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['codeobfuscate']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'codeobfuscate',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Hawchik',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
