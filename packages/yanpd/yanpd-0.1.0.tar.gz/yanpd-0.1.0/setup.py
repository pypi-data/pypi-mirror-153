# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yanpd']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0', 'yangson>=1.4.13,<2.0.0']

setup_kwargs = {
    'name': 'yanpd',
    'version': '0.1.0',
    'description': 'Yet Another Neo4j Python Driver',
    'long_description': None,
    'author': 'Denis',
    'author_email': 'd.mulyalin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
