# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiopyrq']

package_data = \
{'': ['*']}

install_requires = \
['aioredis>=1.2,<2.0']

setup_kwargs = {
    'name': 'aio-py-rq',
    'version': '2.1.1',
    'description': '',
    'long_description': None,
    'author': 'Heureka',
    'author_email': 'vyvoj@heureka.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
