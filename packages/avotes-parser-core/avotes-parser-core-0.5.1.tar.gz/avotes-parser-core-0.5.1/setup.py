# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['avotes_parser',
 'avotes_parser.core',
 'avotes_parser.core.ABI',
 'avotes_parser.core.ABI.utilities']

package_data = \
{'': ['*']}

install_requires = \
['eth-brownie>=1.19.0,<1.20.0',
 'pysha3>=1.0.2,<1.1.0',
 'requests>=2.27.1,<2.28.0',
 'web3>=5.29.1,<5.30.0']

setup_kwargs = {
    'name': 'avotes-parser-core',
    'version': '0.5.1',
    'description': 'Aragon votings parser library',
    'long_description': None,
    'author': 'Dmitri Ivakhnenko',
    'author_email': 'dmit.ivh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
