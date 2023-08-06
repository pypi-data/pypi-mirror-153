# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['showergel', 'showergel.rest']

package_data = \
{'': ['*'], 'showergel': ['www/*', 'www/css/*', 'www/fonts/*', 'www/js/*']}

install_requires = \
['APScheduler>=3.7.0,<4.0.0',
 'Paste>=3.5.0,<4.0.0',
 'arrow>=1.1.0,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'sphinx-rtd-theme>=0.5.1,<0.6.0',
 'sqlalchemy>=1.3.19,<2.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['showergel = showergel:serve',
                     'showergel_install = showergel.install:main']}

setup_kwargs = {
    'name': 'showergel',
    'version': '0.3.0a5',
    'description': 'Companion application for a Liquidsoap radio',
    'long_description': "=========\nShowergel\n=========\n\nShowergel is made to live aside Liquidsoap_:\nwhile a Liquidsoap script creates a radio stream,\nShowergel provides complementary features like playlist logging or occasional\nscheduling, with a (minimalist) Web interface.\nIt is made to run on a Linux box (with systemd) dedicated to your radio stream.\n\nDocumentation and\n`installation instructions <https://showergel.readthedocs.io/en/latest/installing.html>`_\nare hosted\non https://showergel.readthedocs.io/.\n\n**This is work in progress!** We'll welcome both contributions\nand comments, feel free to start a disucssion in the Issues tab.\n\nShowergel have only been tested under Linux.\n\nLicense: GPL3_.\n\nNews\n====\n\n*30/05/2022:* Showergel version 0.3, the first version compliant with Liquidsoap 2.x,\nis coming soon with an all-inclusive installer script.\n\n.. _Liquidsoap: https://www.liquidsoap.info/\n.. _GPL3: https://www.gnu.org/licenses/gpl-3.0.html\n",
    'author': 'Martin Kirchgessner',
    'author_email': 'martin.kirch@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/martinkirch/showergel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
