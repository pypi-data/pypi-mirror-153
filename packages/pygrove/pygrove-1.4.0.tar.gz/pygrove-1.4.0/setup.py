# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pygrove']

package_data = \
{'': ['*'], 'pygrove': ['pygrove.egg-info/*']}

install_requires = \
['pyforest>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'pygrove',
    'version': '1.4.0',
    'description': '',
    'long_description': None,
    'author': 'sileod',
    'author_email': 'damien.sileo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
