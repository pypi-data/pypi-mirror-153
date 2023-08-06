# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyobs_pilar']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=5.0,<6.0', 'pyobs-core>=0.18']

setup_kwargs = {
    'name': 'pyobs-pilar',
    'version': '0.19.0',
    'description': 'pyobs module for Pilar TCS',
    'long_description': None,
    'author': 'Tim-Oliver Husser',
    'author_email': 'thusser@uni-goettingen.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
