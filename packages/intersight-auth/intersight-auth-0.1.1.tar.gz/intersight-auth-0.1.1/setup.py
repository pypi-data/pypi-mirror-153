# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['intersight_auth']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=37.0.2,<38.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'intersight-auth',
    'version': '0.1.1',
    'description': 'Intersight Authentication helper for requests',
    'long_description': None,
    'author': 'Chris Gascoigne',
    'author_email': 'cgascoig@cisco.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
