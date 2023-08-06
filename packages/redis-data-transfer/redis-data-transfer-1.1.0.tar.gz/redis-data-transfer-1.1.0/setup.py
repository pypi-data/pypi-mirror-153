# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redis_data_transfer']

package_data = \
{'': ['*']}

install_requires = \
['redis-py-cluster>=2.0.0,<2.1.0', 'setproctitle>=1.1.10,<1.2.0']

entry_points = \
{'console_scripts': ['redis-data-transfer = redis_data_transfer:main']}

setup_kwargs = {
    'name': 'redis-data-transfer',
    'version': '1.1.0',
    'description': 'Transfer data between a redis instances or clusters',
    'long_description': '[![Build Status](https://travis-ci.org/EDITD/redis_data_transfer.svg?branch=master)](https://travis-ci.org/EDITD/redis_data_transfer)\n[![Pypi Version](https://img.shields.io/pypi/v/redis_data_transfer.svg)](https://pypi.org/project/redis_data_transfer/)\n[![Python Versions](https://img.shields.io/pypi/pyversions/redis_data_transfer.svg)](https://pypi.org/project/redis_data_transfer/)\n\n# Redis data transfer tool\n\nAn easy-to-use tool to transfer data between redis servers or clusters.\n\n### Installation\n```pip install redis-data-transfer```\n\n### Usage\n\nThe command line structure is quite simple:\n```redis-data-transfer [options] your.source.server your.destination.server```\n\nFor details about the options available:\n```redis-data-transfer --help```\n\n### Concepts\n\nThe implementation is made around a pipeline system with queues and subprocesses. The user can\ncontrol the number of parallel subprocesses for each step of the pipeline:\n* A single scanner reads all keys from the source.\n* Checkers look in the destination and filter out any key that already exists. They can be disabled\n  if desired.\n* Readers fetch the content of each key from the source.\n* Writers store the content for each key in the destination.\n\n\n## Development\n\nThe code is [hosted on github](https://github.com/EDITD/redis_data_transfer).\nThe repository uses [poetry](https://python-poetry.org/) for packaging.\nThe project uses [tox](https://tox.wiki/en/latest/) for testing.\n',
    'author': 'EDITED Devs',
    'author_email': 'dev@edited.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/EDITD/redis_data_transfer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
