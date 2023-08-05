# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bilimusic']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.1.1,<10.0.0',
 'eyed3>=0.9.6,<0.10.0',
 'fire>=0.4.0,<0.5.0',
 'moviepy>=1.0.3,<2.0.0',
 'opencv-contrib-python>=4.5.5,<5.0.0',
 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['bilimusic = bilimusic.cli:run']}

setup_kwargs = {
    'name': 'bilimusic',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'aoout',
    'author_email': 'wuz66280@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
