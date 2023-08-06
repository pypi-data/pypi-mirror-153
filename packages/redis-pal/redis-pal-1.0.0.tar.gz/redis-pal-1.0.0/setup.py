# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redis_pal']

package_data = \
{'': ['*']}

install_requires = \
['dill>=0.3.5,<0.4.0', 'redis>=4.0,<5.0']

setup_kwargs = {
    'name': 'redis-pal',
    'version': '1.0.0',
    'description': 'Store things in Redis without worrying about types or anything, just do it!',
    'long_description': None,
    'author': 'Gabriel Gazola Milan',
    'author_email': 'gabriel.gazola@poli.ufrj.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
