# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geoenv', 'geoenv.commands']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['geoenv = geoenv.geoenv:main']}

setup_kwargs = {
    'name': 'geoenv-cli',
    'version': '0.1.0',
    'description': 'CLI for managing a docker based geospatial environment.',
    'long_description': None,
    'author': 'Dustin Sampson',
    'author_email': 'gridcell@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
