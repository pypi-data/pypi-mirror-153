# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_does_redis']

package_data = \
{'': ['*']}

install_requires = \
['redis>=4.3.3,<5.0.0']

setup_kwargs = {
    'name': 'flask-does-redis',
    'version': '0.2.2',
    'description': 'Flask extension to easily reuse redis connection pools',
    'long_description': None,
    'author': 'jthop',
    'author_email': 'jh@mode14.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
