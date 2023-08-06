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
    'version': '0.1.1',
    'description': "GeoEnv is for those that don't want to create a geospatial development environment before you can test out some code you wrote, convert some spatial data or hack on an idea. The cli reduces the steps needed to spin up this working environment by using a docker image that already has a bunch of geospatial tools and libraries preloaded.",
    'long_description': 'GeoEnv\n------\n\nGeoEnv is for those that don\'t want to create a geospatial development environment before you can test out some code you wrote, convert some spatial data or hack on an idea. The cli reduces the steps needed to spin up this working environment by using a docker image that already has a bunch of geospatial tools and libraries preloaded.\n\n\n## Geospatial Working Environment\n\nThe docker environment uses [GeoEnv Docker image](https://github.com/gridcell/geoenv-docker) a preloaded ubuntu docker image that includes:\n\n* gdal cli\n* proj cli\n* aws cli\n* jupyter lab\n* python packages: gdal, cartopy, numpy, rasterio, shapley, pystac, dask and [more](https://github.com/gridcell/geoenv-docker/blob/main/Dockerfile)\n\n\n## Getting Started\n\n`python -m "pip" install geoenv-cli`\n\nOR\n\n`python -m "pip" install --user geoenv-cli`\n\n\n### Using GeoEnv\n\n<img src="https://user-images.githubusercontent.com/915189/171786260-42fb5f9b-b83d-4284-88b7-36a8a97826c2.gif" width="100%"></img> \n\n\n## Contribute\n\nIf you find a bug or missing that library or application you always use, please file an issue or submit a pull request!',
    'author': 'Dustin Sampson',
    'author_email': 'gridcell@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gridcell/geoenv-cli',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
