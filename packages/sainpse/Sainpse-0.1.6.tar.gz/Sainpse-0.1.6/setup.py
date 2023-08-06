# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sainpse', 'sainpse.finance.data']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.1.2,<3.0.0', 'twelvedata>=1.2.4,<2.0.0']

setup_kwargs = {
    'name': 'sainpse',
    'version': '0.1.6',
    'description': 'The Sainpse Institute Utility Python Packages - Bugfixes',
    'long_description': None,
    'author': 'Marcus Madumo',
    'author_email': 'marcusm@sainpse.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
