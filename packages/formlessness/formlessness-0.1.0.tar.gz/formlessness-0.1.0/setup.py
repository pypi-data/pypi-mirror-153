# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['formlessness']

package_data = \
{'': ['*']}

install_requires = \
['pytest-cov>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'formlessness',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Travis Jungroth',
    'author_email': 'jungroth@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
