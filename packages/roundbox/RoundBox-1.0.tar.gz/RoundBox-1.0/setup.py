# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['RoundBox',
 'RoundBox.apps',
 'RoundBox.conf',
 'RoundBox.core',
 'RoundBox.core.cache',
 'RoundBox.core.cache.backends',
 'RoundBox.core.checks',
 'RoundBox.core.cliparser',
 'RoundBox.core.cliparser.commands',
 'RoundBox.core.files',
 'RoundBox.core.hass',
 'RoundBox.core.hass.components',
 'RoundBox.core.hass.components.sensor',
 'RoundBox.core.hass.helpers',
 'RoundBox.core.mail',
 'RoundBox.core.mail.backends',
 'RoundBox.dispatch',
 'RoundBox.utils',
 'RoundBox.utils.backports',
 'RoundBox.utils.backports.strenum',
 'RoundBox.utils.log']

package_data = \
{'': ['*'],
 'RoundBox.conf': ['jobs_template/jobs/*',
                   'jobs_template/jobs/daily/*',
                   'jobs_template/jobs/hourly/*',
                   'jobs_template/jobs/minutely/*',
                   'jobs_template/jobs/monthly/*',
                   'jobs_template/jobs/quarter_hourly/*',
                   'jobs_template/jobs/weekly/*',
                   'jobs_template/jobs/yearly/*']}

install_requires = \
['colorama', 'slugify>=0.0.1,<0.0.2', 'watchdog']

entry_points = \
{'console_scripts': ['roundbox-admin = RoundBox.core.cliparser:exec_from_cli']}

setup_kwargs = {
    'name': 'roundbox',
    'version': '1.0',
    'description': 'A small lightweight framework for IoT applications',
    'long_description': '⚡ RoundBox\n==========\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n![PyPI](https://img.shields.io/pypi/v/roundbox?label=RoundBox&style=plastic)\n![GitHub release (latest by date)](https://img.shields.io/github/v/release/soulraven/roundbox?style=plastic)\n[![Build status](https://img.shields.io/github/workflow/status/soulraven/roundbox/merge-to-main?style=plastic)](https://img.shields.io/github/workflow/status/soulraven/roundbox/merge-to-main)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/roundbox?style=plastic)](https://pypi.org/project/roundbox/)\n[![License](https://img.shields.io/github/license/soulraven/roundbox?style=plastic)](https://img.shields.io/github/license/soulraven/roundbox)\n\n***\n\nA small lightweight framework for IoT applications, with main goal to not reinvent the wheel every time when a small\nproject for IoT device is needed.\n\nThe framework contains all tools necessary to bootstrap and run a command a single time or using linux crontab.\n\nYou can create apps as many as you like and use them for your proper necessity, but consider that each app is liake a\nsmall container with logic.\nEach app has the possibility to host specific commands that will be available  when running manage.py.\n\n### 🎈 Special thanks 🎈\nTo build this framework I have used code inspired by the [Django](https://github.com/django/django) project and also\nfrom [Home Assistant](https://github.com/home-assistant/core) project.\n\nBoth projects have a strong code base and lightweight and port on different projects.\n\n***\n\n### 🔧 Installation\n\nThe easy way to install RoundBox framework is with [pip]\n\n```bash\n$ pip install roundbox\n```\n\nIf you want to install RoundBox from GitHub use:\n\n```bash\n$ pip install git+https://github.com/soulraven/roundbox.git\n```\n\nFor more detailed install instructions see how [Install] and configure the framework.\n\n***\n\n### ➿ Variables\n\n- set the ROUNDBOX_COLORS environment variable to specify the palette you want to use. For example,\nto specify the light palette under a Unix or OS/X BASH shell, you would run the following at a command prompt:\n\n```bash\nexport ROUNDBOX_COLORS="light"\n```\n\n***\n\n### 🖇 Library used\n\nA more detailed list you will find here: [Libraries](https://soulraven.github.io/roundbox/libraries/)\n\n***\n\n### 🌍 Contributions\n\nContributions of all forms are welcome :)\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## 📝 License\n\nThis project is licensed under [GPLv3].\n\n## 👀 Author\n\nZaharia Constantin, my [GitHub profile] and [GitHub Page]\n\n[GitHub profile]: https://github.com/soulraven/\n[Github Page]: https://soulraven.github.io/\n[GNU General Public License]: https://www.gnu.org/licenses/quick-guide-gplv3.html\n[pip]: https://pip.pypa.io/en/stable/\n[GPLv3]: https://soulraven.github.io/roundbox/license\n[Install]: https://soulraven.github.io/roundbox/user-guide/topics/install\n',
    'author': 'Zaharia Constantin',
    'author_email': 'layout.webdesign@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/soulraven/roundbox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
