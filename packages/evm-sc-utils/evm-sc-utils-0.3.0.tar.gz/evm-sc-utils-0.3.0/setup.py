# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['evm_sc_utils']

package_data = \
{'': ['*']}

install_requires = \
['web3>=5.27.0,<6.0.0']

setup_kwargs = {
    'name': 'evm-sc-utils',
    'version': '0.3.0',
    'description': 'Utilities that are helpful when developing Ethereum Virtual Machine Smart Contracts with Python.',
    'long_description': None,
    'author': 'mpeyfuss',
    'author_email': '82735893+mpeyfuss@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
