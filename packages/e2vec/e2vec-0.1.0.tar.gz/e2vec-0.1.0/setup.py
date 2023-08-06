# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['e2vec']

package_data = \
{'': ['*']}

install_requires = \
['timm>=0.5.4,<0.6.0']

setup_kwargs = {
    'name': 'e2vec',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'An Pham',
    'author_email': 'ancs21.ps@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.12,<4.0.0',
}


setup(**setup_kwargs)
