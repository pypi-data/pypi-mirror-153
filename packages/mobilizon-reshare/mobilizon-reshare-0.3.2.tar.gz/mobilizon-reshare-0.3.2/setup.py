# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mobilizon_reshare',
 'mobilizon_reshare.cli',
 'mobilizon_reshare.cli.commands',
 'mobilizon_reshare.cli.commands.format',
 'mobilizon_reshare.cli.commands.list',
 'mobilizon_reshare.cli.commands.publish',
 'mobilizon_reshare.cli.commands.pull',
 'mobilizon_reshare.cli.commands.recap',
 'mobilizon_reshare.cli.commands.retry',
 'mobilizon_reshare.cli.commands.start',
 'mobilizon_reshare.config',
 'mobilizon_reshare.event',
 'mobilizon_reshare.formatting',
 'mobilizon_reshare.main',
 'mobilizon_reshare.mobilizon',
 'mobilizon_reshare.models',
 'mobilizon_reshare.publishers',
 'mobilizon_reshare.publishers.platforms',
 'mobilizon_reshare.publishers.templates',
 'mobilizon_reshare.storage',
 'mobilizon_reshare.storage.query']

package_data = \
{'': ['*'], 'mobilizon_reshare': ['migrations/models/*']}

install_requires = \
['Jinja2>=3.1,<3.2',
 'aerich>=0.6,<0.7',
 'aiosqlite>=0.17,<0.18',
 'appdirs>=1.4,<1.5',
 'arrow>=1.1,<1.2',
 'beautifulsoup4>=4.10,<4.11',
 'click>=8.0,<8.1',
 'dynaconf>=3.1,<3.2',
 'facebook-sdk>=3.1,<3.2',
 'markdownify>=0.10,<0.11',
 'requests>=2.26,<2.27',
 'tortoise-orm>=0.18,<0.19',
 'tweepy>=4.4,<4.5']

entry_points = \
{'console_scripts': ['mobilizon-reshare = '
                     'mobilizon_reshare.cli.cli:mobilizon_reshare']}

setup_kwargs = {
    'name': 'mobilizon-reshare',
    'version': '0.3.2',
    'description': 'A suite to reshare Mobilizon events on a broad selection of platforms',
    'long_description': "[![CI](https://github.com/Tech-Workers-Coalition-Italia/mobilizon-reshare/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/Tech-Workers-Coalition-Italia/mobilizon-reshare/actions/workflows/main.yml)\n\nThe goal of `mobilizon_reshare` is to provide a suite to reshare Mobilizon events on a broad selection of platforms. This\ntool enables an organization to automate their social media strategy in regards\nto events and their promotion. \n\n# Platforms\n\n`mobilizon-reshare` currently supports the following social platforms:\n\n- Facebook\n- Mastodon\n- Twitter\n- Telegram\n- Zulip\n\n# Usage\n\n## Scheduling and temporal logic\n\nThe tool is designed to work in combination with a scheduler that executes it at\nregular intervals. `mobilizon_reshare` allows fine-grained control over the logic to decide when\nto publish an event, with the minimization of human effort as its first priority.\n\n## Installation\n\n`mobilizon_reshare` is distributed through [Pypi](https://pypi.org/project/mobilizon-reshare/) and [DockerHub](https://hub.docker.com/r/fishinthecalculator/mobilizon-reshare). Use\n\n```shell\n$ pip install mobilizon-reshare\n```\n\nto install the tool in your system or virtualenv.\n\nThis should install the command `mobilizon-reshare` in your system. Use it to access the CLI and discover the available\ncommands and their description.\n\n### Guix package\n\nIf you run Guix you can install `mobilizon-reshare` by adding our [Guix channel](https://github.com/fishinthecalculator/mobilizon-reshare-guix#configure) to your `.config/guix/channels.scm`.\n\n\n\n\nTo run `mobilizon-reshare` from master you can run the following command from the root of the repository:\n\n``` shell\n$ guix time-machine -C channels-lock.scm -- install -L . mobilizon-reshare.git\n```\n\n## Run on your local system\n\nOnce you have installed `mobilizon_reshare` you can schedule the refresh from Mobilizon with your system's `cron`:\n\n```bash\n$ sudo crontab -l\n*/15 * * * * mobilizon-reshare start\n```\n\n## Deploying through Docker Compose\n\nTo run `mobilizon_reshare` in a production environment you can use the image published to DockerHub. We also provide an example [`docker-compose.yml`](https://github.com/Tech-Workers-Coalition-Italia/mobilizon-reshare/blob/master/docker-compose.yml).\n\n# Contributing\n\nWe welcome contributions from anybody. Currently our process is not structured but feel free to open or take issues through Github in case you want to help us. We have setup some instructions to setup a development environment [here](https://github.com/Tech-Workers-Coalition-Italia/mobilizon-reshare/blob/master/doc/contributing.md).\n",
    'author': 'Simone Robutti',
    'author_email': 'simone.robutti@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Tech-Workers-Coalition-Italia/mobilizon-reshare',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
