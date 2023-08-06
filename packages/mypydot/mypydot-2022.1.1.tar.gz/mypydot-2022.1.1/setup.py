# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mypydot', 'mypydot.src']

package_data = \
{'': ['*'],
 'mypydot': ['template/*',
             'template/language/*',
             'template/language/go/*',
             'template/language/java/*',
             'template/language/python/*',
             'template/os/*',
             'template/shell/*',
             'template/shell/bash/*',
             'template/shell/zim/*',
             'template/shell/zsh/*',
             'template/tools/docker/*',
             'template/tools/editors/*',
             'template/tools/editors/vim/*',
             'template/tools/git/*']}

install_requires = \
['PyYAML==6.0', 'emoji>=1.6.1,<2.0.0']

entry_points = \
{'console_scripts': ['mypydot = mypydot.src.main:entry_point']}

setup_kwargs = {
    'name': 'mypydot',
    'version': '2022.1.1',
    'description': 'Python package to manage your dotfiles',
    'long_description': '[![PyPI version](https://badge.fury.io/py/mypydot.svg)](https://badge.fury.io/py/mypydot)\n![CI](https://github.com/andres-ortizl/mypydot/actions/workflows/main.yml/badge.svg)\n[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=mypydot&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=mypydot)\n[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=mypydot&metric=coverage)](https://sonarcloud.io/summary/new_code?id=mypydot)\n[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=mypydot&metric=bugs)](https://sonarcloud.io/summary/new_code?id=mypydot)\n\n## Mypydot\n\nMypydot is a tool created for managing your dotfiles using a Python application\n\n# Motivation\n\nI just wanted the basic functionality to manage my own dotfiles. I decided to do it in Python because It seems more\nnatural\nto me rather than do It using shell scripting.\n\n## Install\n\n```pip install mypydot```\n\n## Instructions\n\n### Create new dotfiles\n\nUsing it for the first time : ```mypydot --option create``` . This command will create a new folder called .mypydotfiles\nin your $HOME directory. In this folder you will find the following folder structure :\n\n| Folder     |                                                                                                                               | \n|------------|-------------------------------------------------------------------------------------------------------------------------------|\n| `language` | In case you want to save some dotfiles related with your favourite programming languages                                      |  \n| `os`       | Operating system dotfiles                                                                                                     |  \n| `shell`    | Everything related to bash & zsh, etc..                                                                                       |  \n| `tools`    | Docker, Git, Editors, etc. You can also find here a few almost empty scripts for storing your aliases, exports and functions. |  \n| `conf.yml` | This file contains every file that you want to track in your dotfiles repository, feel free to add & remove symlinks !        |  \n\nOnce you run this process you will notice that you have a few new lines your .bashrc and in your .zshrc\n\n```\nexport MYPYDOTFILES=/Users/username/.mypydotfiles\nsource $MYPYDOTFILES/shell/main.sh\n```\n\nThis lines will be used to source yours aliases, exports and functions to be available in your terminal.\nBesides that, nothing else is edited.\n\n### Resync dotfiles ( for restoring or sync new files)\n\n```mypydot --option sync``` . This will iterate again over your .conf.yml file trying to sync new dotfiles.\n\n# References\n\nhttps://github.com/mathiasbynens/dotfiles\n\nhttps://github.com/CodelyTV/dotly\n\nhttps://github.com/denisidoro/dotfiles\n\nhttps://github.com/webpro/awesome-dotfiles\n\nThank you!',
    'author': 'Andrés Ortiz',
    'author_email': 'andrs.ortizl@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andres-ortizl/mypydot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
