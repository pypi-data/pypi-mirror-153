# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wordlecli']

package_data = \
{'': ['*']}

install_requires = \
['DateTime>=4.4,<5.0',
 'pyperclip>=1.8.2,<2.0.0',
 'rich>=11.2.0,<12.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['wordle = wordlecli.cli:main']}

setup_kwargs = {
    'name': 'wordlecli',
    'version': '0.2.2',
    'description': 'wordle, but in the command line',
    'long_description': '<h2 align="center"> ━━━━━━  ❖  ━━━━━━ </h2>\n\n<!-- BADGES -->\n<div align="center">\n   <p></p>\n   \n   <img src="https://img.shields.io/github/stars/dotzenith/wordle-cli?color=F8BD96&labelColor=302D41&style=for-the-badge">   \n\n   <img src="https://img.shields.io/github/forks/dotzenith/wordle-cli?color=DDB6F2&labelColor=302D41&style=for-the-badge">   \n\n   <img src="https://img.shields.io/github/repo-size/dotzenith/wordle-cli?color=ABE9B3&labelColor=302D41&style=for-the-badge">\n   \n   <img src="https://badges.pufler.dev/visits/dotzenith/wordle-cli?style=for-the-badge&color=96CDFB&logoColor=white&labelColor=302D41"/>\n   <br>\n</div>\n\n<p/>\n\n---\n\n### ❖ Information \n\n  wordle-cli is, as the name suggests, wordle in the command-line. There are no fancy gui/tui elements, just a simple and minimalistic way to play wordle :)\n\n  <img src="assets/wordle.gif" alt="wordle preview">\n\n---\n\n### ❖ Installation\n\n> Install from pip\n```sh\n$ pip3 install wordlecli\n```\n\n> Install from source\n- First, install [poetry](https://python-poetry.org/)\n```sh\n$ git clone https://github.com/ZenithDS/wordle-cli.git\n$ cd wordle-cli\n$ poetry build\n$ pip3 install ./dist/wordlecli-0.2.2.tar.gz\n```\n\n### ❖ Usage \n\nPlaying wordle in the command-line is as simple as running the following command:\n\n```sh\n$ wordle\n```\n\nBut if your addiction to wordle needs more, you can also play an older wordle by specifying it\'s number\n\n```sh\n$ wordle 240\n```\n\nThe on-screen keyboard can be turned off using the `--hard` option\n\n```sh\n$ wordle --hard\n```\n\n---\n\n### ❖ What\'s New? \n0.2.2 - Updated `words.py` to be consistent with the official wordle\n\n---\n\n<div align="center">\n\n   <img src="https://img.shields.io/static/v1.svg?label=License&message=MIT&color=F5E0DC&labelColor=302D41&style=for-the-badge">\n\n</div>\n\n',
    'author': 'ZenithDS',
    'author_email': None,
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
