# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['HcoopMeetbot', 'hcoopmeetbotlogic']

package_data = \
{'': ['*'], 'hcoopmeetbotlogic': ['templates/*']}

install_requires = \
['attrs>=21.2.0,<22.0.0',
 'cattrs>=22.1.0,<23.0.0',
 'click>=8.1.3,<9.0.0',
 'genshi>=0.7.5,<0.8.0',
 'importlib-metadata>=4.11.4,<5.0.0',
 'limnoria>=2021.01.15,<2022.0.0',
 'pytz>=2021.3,<2022.0']

entry_points = \
{'console_scripts': ['meetbot = hcoopmeetbotlogic.cli:meetbot'],
 'limnoria.plugins': ['HcoopMeetbot = HcoopMeetbot:plugin']}

setup_kwargs = {
    'name': 'hcoop-meetbot',
    'version': '0.6.0',
    'description': 'Plugin for Limnoria to help run IRC meetings',
    'long_description': '# HCoop Meetbot Plugin\n\n[![pypi](https://img.shields.io/pypi/v/hcoop-meetbot.svg)](https://pypi.org/project/hcoop-meetbot/)\n[![license](https://img.shields.io/pypi/l/hcoop-meetbot.svg)](https://github.com/pronovic/hcoop-meetbot/blob/master/LICENSE)\n[![wheel](https://img.shields.io/pypi/wheel/hcoop-meetbot.svg)](https://pypi.org/project/hcoop-meetbot/)\n[![python](https://img.shields.io/pypi/pyversions/hcoop-meetbot.svg)](https://pypi.org/project/hcoop-meetbot/)\n[![Test Suite](https://github.com/pronovic/hcoop-meetbot/workflows/Test%20Suite/badge.svg)](https://github.com/pronovic/hcoop-meetbot/actions?query=workflow%3A%22Test+Suite%22)\n[![docs](https://readthedocs.org/projects/hcoop-meetbot/badge/?version=stable&style=flat)](https://hcoop-meetbot.readthedocs.io/en/stable/)\n[![coverage](https://coveralls.io/repos/github/pronovic/hcoop-meetbot/badge.svg?branch=master)](https://coveralls.io/github/pronovic/hcoop-meetbot?branch=master)\n\n[hcoop-meetbot](https://github.com/pronovic/hcoop-meetbot) is a plugin for [Limnoria](https://github.com/ProgVal/Limnoria), a bot framework for IRC.  It is designed to help run meetings on IRC.  It was originally written for quarterly board meetings at [HCoop](https://hcoop.net), when Ken was on the board there.\n\nThe code is based in part on the [MeetBot](https://github.com/rkdarst/MeetBot/) plugin for Supybot written by Richard Darst. Supybot is the predecessor to Limnoria.  Richard\'s MeetBot was "inspired by the original MeetBot, by Holger Levsen, which was itself a deri vative of Mootbot by the Ubuntu Scribes team".  So, this code has a relatively long history.  For this version, much of the plugin was rewritten using Python 3, but it generally follows the pattern set by Richard\'s original code.  \n\nSee the [user documentation](https://hcoop-meetbot.readthedocs.io/en/stable/) for more information about how to use the plugin, including installation instructions.\n\n',
    'author': 'Kenneth J. Pronovici',
    'author_email': 'pronovic@ieee.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/hcoop-meetbot/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
