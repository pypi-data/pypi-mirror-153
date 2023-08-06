# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wush',
 'wush.argument',
 'wush.cli',
 'wush.common',
 'wush.completion',
 'wush.config',
 'wush.web']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.0.1,<3.0.0',
 'PyYAML>=6.0,<7.0',
 'browsercookie>=0.7.7,<0.8.0',
 'csarg>=0.1.0,<0.2.0',
 'loguru>=0.6.0,<0.7.0',
 'prompt-toolkit>=3.0.29,<4.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=10.6.0,<11.0.0',
 'w3lib>=1.22.0,<2.0.0',
 'wpy>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['wush = wush.cli.main:main']}

setup_kwargs = {
    'name': 'wush',
    'version': '0.2.3',
    'description': 'Useful api client on terminal',
    'long_description': None,
    'author': 'wxnacy',
    'author_email': 'wxnacy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
