# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arbache_authentication',
 'arbache_authentication.tests',
 'arbache_authentication.tests.mocks']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2.13,<4.0.0',
 'djangorestframework>=3.13.1,<4.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'arbache-authentication',
    'version': '1.0.2',
    'description': 'Pacote de autenticações das aplicações Arbache',
    'long_description': None,
    'author': 'Willames',
    'author_email': 'williames@arbache.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.7,<4.0.0',
}


setup(**setup_kwargs)
