# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlschm']

package_data = \
{'': ['*']}

modules = \
['py']
entry_points = \
{'console_scripts': ['corpus = scripts:main']}

setup_kwargs = {
    'name': 'sqlschm',
    'version': '0.6.0',
    'description': 'A SQLite Schema parser',
    'long_description': None,
    'author': 'Victorien Elvinger',
    'author_email': 'victorien.elvinger@inria.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/coast-team/sqlschm',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
