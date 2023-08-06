# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rainbowlog']

package_data = \
{'': ['*']}

install_requires = \
['ansicolors>=1.1.8,<2.0.0']

setup_kwargs = {
    'name': 'rainbowlog',
    'version': '0.1.0',
    'description': 'Format your python logs with colours based on the log levels.',
    'long_description': None,
    'author': 'Abraham Murciano',
    'author_email': 'abrahammurciano@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
