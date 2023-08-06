# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['curses_playlist']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'moviepy>=1.0.3,<2.0.0', 'windows-curses>=2.3.0,<3.0.0']

entry_points = \
{'console_scripts': ['plist = curses_playlist.plist:main']}

setup_kwargs = {
    'name': 'curses-playlist',
    'version': '0.1.3',
    'description': 'curses based interactive playlist creation for videos',
    'long_description': '# plist\ncurses based interactive playlist creation for video files.\n\n# usage\n\n```\nplist.exe --playlist c:\\tmp\\test.m3u --working-directory Z:\\movies\n```\n\n# docs\n\nInteractively create a `playlist.m3u` then launch it using `vlc.exe`. \nAutomatically loads last playlist on startup.\nThere are 2 modes which you can toggle using the `ESC` key:\n```\n[INPUT: ENTER - add | ESC - CMD] \n[CMD: m - mod | q | w | p - play | r - reset]\n```\n\nIn `INPUT` Mode, filenames in the playlist are searched for substrings that you enter, separated by a single whitespace. \n\nE.g.: `rick` `morty` `s01e01` would yield all filenames that contain all 3 strings.\n\nIn `CMD` mode you have the following options:\n\n* `m` move\n  * `j` navigate/move down\n  * `k` navigate/move up\n  * `d` del \n  * `m` toggle navigate/move\n* `p` play: start vlc player with playlist\n* `r` reset: reset the playlist\n* `q` quit: doing nothing\n\n# repo\n\nhttps://github.com/dosnpfand/curses-playlist\n',
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
