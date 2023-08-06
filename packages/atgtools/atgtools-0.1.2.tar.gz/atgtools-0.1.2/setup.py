# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['atgtools']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.2,<9.0.0', 'pandas>=1.4.1,<2.0.0', 'rich>=12.4.4,<13.0.0']

entry_points = \
{'console_scripts': ['atg = atgtools.atg:main']}

setup_kwargs = {
    'name': 'atgtools',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'zorbax',
    'author_email': 'otto94@gmail.com',
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
