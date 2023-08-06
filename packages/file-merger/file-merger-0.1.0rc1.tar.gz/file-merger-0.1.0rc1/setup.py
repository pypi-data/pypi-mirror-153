# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['file_merger']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0']

entry_points = \
{'console_scripts': ['file-merger = file_merger:main']}

setup_kwargs = {
    'name': 'file-merger',
    'version': '0.1.0rc1',
    'description': 'Merge multiple text files into one',
    'long_description': None,
    'author': 'Ilia',
    'author_email': 'istudyatuni@gmail.com',
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
