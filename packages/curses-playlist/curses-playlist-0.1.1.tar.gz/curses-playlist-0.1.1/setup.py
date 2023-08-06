# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['curses_playlist']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'moviepy>=1.0.3,<2.0.0', 'windows-curses>=2.3.0,<3.0.0']

entry_points = \
{'console_scripts': ['plist = plist.plist:main']}

setup_kwargs = {
    'name': 'curses-playlist',
    'version': '0.1.1',
    'description': 'curses based interactive playlist creation for videos',
    'long_description': None,
    'author': 'dominicmai',
    'author_email': 'dr.dosn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
