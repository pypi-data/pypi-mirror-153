# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typed_graphql']

package_data = \
{'': ['*']}

install_requires = \
['docstring-parser>=0.14.1,<0.15.0',
 'graphql-core==3.2.1',
 'pytypes>=1.0b10,<2.0',
 'typing-inspect>=0.7.1,<0.8.0']

setup_kwargs = {
    'name': 'typed-graphql',
    'version': '0.16.0.dev0',
    'description': 'Use types to have a simpler graphql implementation',
    'long_description': None,
    'author': 'Willem Thiart',
    'author_email': 'himself@willemthiart.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
