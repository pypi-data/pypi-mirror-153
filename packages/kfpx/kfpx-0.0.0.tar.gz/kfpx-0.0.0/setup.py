# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kfpx']

package_data = \
{'': ['*']}

install_requires = \
['kfp>=1.8.12,<2.0.0']

setup_kwargs = {
    'name': 'kfpx',
    'version': '0.0.0',
    'description': '',
    'long_description': None,
    'author': 'Hao Xin',
    'author_email': 'haoxinst@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
