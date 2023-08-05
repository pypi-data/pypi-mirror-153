# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['avotes_parser', 'avotes_parser.cli']

package_data = \
{'': ['*']}

install_requires = \
['avotes-parser-core>=0.5.1,<0.6.0',
 'eth-brownie>=1.19.0,<1.20.0',
 'pysha3>=1.0.2,<1.1.0',
 'requests>=2.27.1,<2.28.0',
 'web3>=5.29.1,<5.30.0']

entry_points = \
{'console_scripts': ['avotes-parser = avotes_parser.cli.__main__:main']}

setup_kwargs = {
    'name': 'avotes-parser-cli',
    'version': '0.5.1',
    'description': 'Aragon votings parser CLI',
    'long_description': None,
    'author': 'Dmitri Ivakhnenko',
    'author_email': 'dmit.ivh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
