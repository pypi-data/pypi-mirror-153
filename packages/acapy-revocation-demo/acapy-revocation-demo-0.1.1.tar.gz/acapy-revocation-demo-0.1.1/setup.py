# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['acapy_revocation_demo', 'acapy_revocation_demo.controller']

package_data = \
{'': ['*']}

install_requires = \
['acapy-client==0.7.3.post0', 'aiohttp>=3.8.1,<4.0.0', 'blessings>=1.7,<2.0']

setup_kwargs = {
    'name': 'acapy-revocation-demo',
    'version': '0.1.1',
    'description': 'Demonstrate Indy AnonCreds revocation using ACA-Py',
    'long_description': None,
    'author': 'Daniel Bluhm',
    'author_email': 'dbluhm@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
