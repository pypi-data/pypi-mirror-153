# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rtbhouse_sdk']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.18.4']

setup_kwargs = {
    'name': 'rtbhouse-sdk',
    'version': '8.1.0',
    'description': 'RTB House SDK',
    'long_description': None,
    'author': 'RTB House Apps Team',
    'author_email': 'apps@rtbhouse.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rtbhouse-apps/rtbhouse-python-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*',
}


setup(**setup_kwargs)
