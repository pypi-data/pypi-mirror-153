# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['intentron', 'intentron.stages', 'intentron.utils']

package_data = \
{'': ['*']}

install_requires = \
['alive-progress>=2.4.1,<3.0.0',
 'click>=8.1.3,<9.0.0',
 'loguru>=0.6.0,<0.7.0',
 'matplotlib>=3.5.2,<4.0.0',
 'mediapipe>=0.8',
 'opencv-python>=4.5.5,<5.0.0',
 'pandas>=1.4.2,<2.0.0',
 'scikit-learn>=1.1.1,<2.0.0',
 'scipy>=1.8.1,<2.0.0',
 'seaborn>=0.11.2,<0.12.0']

setup_kwargs = {
    'name': 'intentron',
    'version': '0.1.7',
    'description': '',
    'long_description': None,
    'author': 'catsudo',
    'author_email': 'catsudo@nous.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
