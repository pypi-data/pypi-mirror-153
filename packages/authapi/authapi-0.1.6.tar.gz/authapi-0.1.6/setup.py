# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['authapi',
 'authapi.providers',
 'authapi.providers.facebook',
 'authapi.providers.google',
 'authapi.providers.microsoft']

package_data = \
{'': ['*'], 'authapi': ['templates/*']}

install_requires = \
['Flask>=2.1.2,<3.0.0',
 'cffi>=1.15.0,<2.0.0',
 'pyOpenSSL>=22.0.0,<23.0.0',
 'pydantic>=1.9.1,<2.0.0',
 'requests-oauthlib>=1.3.1,<2.0.0']

setup_kwargs = {
    'name': 'authapi',
    'version': '0.1.6',
    'description': '',
    'long_description': None,
    'author': 'Manuel Castillo',
    'author_email': 'manucalop@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
