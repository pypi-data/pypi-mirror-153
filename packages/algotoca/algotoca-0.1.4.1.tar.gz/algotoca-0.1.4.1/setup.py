# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['algotoca', 'algotoca.grafos', 'algotoca.grafos.coloracao']

package_data = \
{'': ['*']}

install_requires = \
['cairocffi>=1.3.0,<2.0.0', 'igraph>=0.9.9,<0.10.0']

setup_kwargs = {
    'name': 'algotoca',
    'version': '0.1.4.1',
    'description': '',
    'long_description': None,
    'author': 'WLAraujo',
    'author_email': 'lima.wesleyaraujo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
