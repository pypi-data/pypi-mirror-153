# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tapioca_teamculture']

package_data = \
{'': ['*']}

install_requires = \
['tapioca-wrapper>=2.1.0,<3.0.0']

setup_kwargs = {
    'name': 'tapioca-teamculture',
    'version': '0.1.9',
    'description': 'TeamCulture API wrapper using tapioca',
    'long_description': None,
    'author': 'Felipe Guilherme Sabino',
    'author_email': 'felipe@sabino.pro',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
