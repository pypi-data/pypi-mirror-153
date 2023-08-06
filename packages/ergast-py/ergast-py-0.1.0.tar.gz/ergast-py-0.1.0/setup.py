# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ergast_py', 'ergast_py.constants', 'ergast_py.models']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0', 'uritemplate>=4.1.1,<5.0.0']

setup_kwargs = {
    'name': 'ergast-py',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Samuel Roach',
    'author_email': 'samuelroach.2000@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
