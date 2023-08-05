# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gofilepy']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.0,<3.0', 'rich>=10.0,<11.0']

entry_points = \
{'console_scripts': ['gofile = gofilepy:gofile.main']}

setup_kwargs = {
    'name': 'gofilepy',
    'version': '0.2.0',
    'description': 'Upload files to Gofile.io',
    'long_description': None,
    'author': 'Alyetama',
    'author_email': '56323389+Alyetama@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
