# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['disquest_utils']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.36,<2.0.0',
 'asyncpg>=0.25.0,<0.26.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'uvloop>=0.16.0,<0.17.0']

setup_kwargs = {
    'name': 'disquest-utils',
    'version': '1.0.5',
    'description': "A set of async utils for Miku's DisQuest Cog",
    'long_description': '<div align=center>\n\n\n# DisQuest-Utils\n\n![PyPI](https://img.shields.io/pypi/v/disquest-utils?label=PyPi&logo=pypi&logoColor=white) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/disquest-utils?label=Python&logo=python&logoColor=white)\n![PyPI - License](https://img.shields.io/pypi/l/disquest-utils?label=License&logo=github&logoColor=white)\n\nA set of async utils for DisQuest\n\n<div align=left>\n\n# Info\n\nDisQuest is an base system for storing and giving users on Discord xp. This is just the base set of coroutines needed in order to use DisQuest. DisQuest uses PostgreSQL.\n',
    'author': 'No767',
    'author_email': '73260931+No767@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/No767/DisQuest-Utils',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
