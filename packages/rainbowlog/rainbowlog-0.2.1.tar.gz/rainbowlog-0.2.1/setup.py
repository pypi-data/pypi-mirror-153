# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rainbowlog']

package_data = \
{'': ['*']}

install_requires = \
['ansicolors>=1.1.8,<2.0.0', 'importlib-metadata>=4.11.4,<5.0.0']

setup_kwargs = {
    'name': 'rainbowlog',
    'version': '0.2.1',
    'description': 'Format your python logs with colours based on the log levels.',
    'long_description': "# Rainbow Log\n\nFormat your python logs with colours based on the log levels.\n\n## Installation\n\n\tpip install rainbowlog\n\n## Usage\n\nHere's a basic example of a script that logs colorfully to the console, but regularly to a file.\n\n```python\nimport logging\nimport rainbowlog\n\nlogger = logging.getLogger(__name__)\n\n# This one will write to the console\nstream_handler = logging.StreamHandler()\n\n# This one will write to a file\nfile_handler = logging.FileHandler('output.log')\n\n# Here we decide how we want the logs to look like\nformatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')\n\n# We want the stream handler to be colorful\nstream_handler.setFormatter(rainbowlog.Formatter(formatter))\n\n# We don't want the file handler to be colorful\nfile_handler.setFormatter(formatter)\n\n# Finally we add the handlers to the logger\nlogger.addHandler(stream_handler)\nlogger.addHandler(file_handler)\n\nif __name__ == '__main__':\n\tlogger.debug('This is a debug message')\n\tlogger.info('This is an info message')\n\tlogger.warning('This is a warning message')\n\tlogger.error('This is an error message')\n\tlogger.critical('This is a critical message')\n```\n\n## Docs\n\nYou can find the documentation [here](https://abrahammurciano.github.io/rainbowlog/rainbowlog)\n",
    'author': 'Abraham Murciano',
    'author_email': 'abrahammurciano@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abrahammurciano/rainbowlog',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
