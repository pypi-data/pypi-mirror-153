# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qaga',
 'qaga.mutation',
 'qaga.recombination',
 'qaga.selection',
 'qaga.startup',
 'qaga.termination',
 'qaga.testing']

package_data = \
{'': ['*']}

install_requires = \
['dimod>=0.10.15,<0.11.0',
 'dwave-neal>=0.5.9,<0.6.0',
 'dwave-system>=1.11.0,<2.0.0',
 'toolz>=0.11.2,<0.12.0']

setup_kwargs = {
    'name': 'qaga',
    'version': '0.0.3.post3',
    'description': '',
    'long_description': None,
    'author': 'dokunogakusha',
    'author_email': '94387179+dokunogakusha@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
