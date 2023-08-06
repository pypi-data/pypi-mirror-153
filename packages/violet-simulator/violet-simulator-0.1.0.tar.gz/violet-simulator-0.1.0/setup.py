# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vi']

package_data = \
{'': ['*']}

install_requires = \
['polars>=0.13.38,<0.14.0',
 'pygame>=2.1.2,<3.0.0',
 'pyserde[toml]>=0.7.3,<0.8.0']

setup_kwargs = {
    'name': 'violet-simulator',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Storm Timmermans',
    'author_email': 'stormtimmermans@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/m-rots/violet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
