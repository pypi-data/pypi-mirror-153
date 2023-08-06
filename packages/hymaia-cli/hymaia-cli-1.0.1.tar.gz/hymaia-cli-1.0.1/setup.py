# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hymaia_cli', 'hymaia_cli.command', 'hymaia_cli.utils']

package_data = \
{'': ['*'], 'hymaia_cli': ['resources/*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['hymaia_cli = hymaia_cli.main:main']}

setup_kwargs = {
    'name': 'hymaia-cli',
    'version': '1.0.1',
    'description': '',
    'long_description': None,
    'author': 'Elhadi Cherifi',
    'author_email': 'elhadi.cherifi@hymaia.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
