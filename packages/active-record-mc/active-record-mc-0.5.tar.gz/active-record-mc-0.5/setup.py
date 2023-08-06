# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ActiveRecord']

package_data = \
{'': ['*']}

install_requires = \
['PyGObject>=3.42.0,<4.0.0', 'tomlkit<1.0.0']

setup_kwargs = {
    'name': 'active-record-mc',
    'version': '0.5',
    'description': 'Simple ORM for basic operations in SQLite databases',
    'long_description': "This module implements a simple ORM for basic operations in SQLite databases.\n\nThe module is derived from a working example of the active record pattern created\nby Chris Mitchell to supplement a talk given at the Oregon Academy of Sciences\nmeeting on January 26, 2011.\n\nThe example is published on GitHub as \n\nhttps://github.com/ChrisTM/Active-Record-Example-for-a-Gradebook\n\nand the code is understood to be freely available under the MIT license as above.\n\nThe original code has been modified so that\n\n* The column names in the selected table are obtained automatically by introspection of the database.\n* The primary key column is no longer required to be 'pk'.\n* Errors are reported via a dialog box.\n\n",
    'author': 'Chris Brown',
    'author_email': 'chris@marcrisoft.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
