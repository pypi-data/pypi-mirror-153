# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_photo_colorizer']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.4,<2.0.0', 'opencv-python>=4.5.5,<5.0.0', 'wget>=3.2,<4.0']

setup_kwargs = {
    'name': 'py-photo-colorizer',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'RCJacH',
    'author_email': 'RCJacH@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
