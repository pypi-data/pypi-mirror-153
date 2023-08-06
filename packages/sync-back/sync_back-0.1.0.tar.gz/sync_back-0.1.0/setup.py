# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sync_back']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'rich>=12.4.4,<13.0.0']

entry_points = \
{'console_scripts': ['bsync = sync_back:term.cli']}

setup_kwargs = {
    'name': 'sync-back',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Deepio',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
