# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gtklara']

package_data = \
{'': ['*']}

install_requires = \
['PyGObject>=3.42.1,<4.0.0']

setup_kwargs = {
    'name': 'gtklara',
    'version': '0.0.3',
    'description': 'initialize operating system on gtklara',
    'long_description': None,
    'author': 'Clay Risser',
    'author_email': 'clayrisser@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.6,<4.0.0',
}


setup(**setup_kwargs)
