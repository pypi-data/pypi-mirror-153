# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pinject_design', 'pinject_design.di', 'pinject_design.viz']

package_data = \
{'': ['*']}

install_requires = \
['cloudpickle',
 'cytoolz',
 'expression',
 'loguru',
 'makefun',
 'pampy',
 'pinject',
 'returns',
 'tabulate']

setup_kwargs = {
    'name': 'pinject-design',
    'version': '0.1.17',
    'description': 'immutable wrapper for pinject',
    'long_description': None,
    'author': 'proboscis',
    'author_email': 'nameissoap@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
