# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hal', 'hal.actor', 'hal.helpers', 'hal.macros']

package_data = \
{'': ['*'], 'hal': ['etc/*', 'etc/scripts/*']}

install_requires = \
['click-default-group>=1.2.2,<2.0.0',
 'numpy>=1.22.1,<2.0.0',
 'sdss-clu>=1.4.0,<2.0.0',
 'sdsstools>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['hal = hal.__main__:hal']}

setup_kwargs = {
    'name': 'sdss-hal',
    'version': '0.2.0',
    'description': 'High-level observing tool for SDSS-V (replaces SOP)',
    'long_description': '# HAL\n\n![Versions](https://img.shields.io/badge/python->3.9-blue)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Documentation Status](https://readthedocs.org/projects/sdss-hal/badge/?version=latest)](https://sdss-hal.readthedocs.io/en/latest/?badge=latest)\n[![Test](https://github.com/sdss/hal/actions/workflows/test.yml/badge.svg)](https://github.com/sdss/hal/actions/workflows/test.yml)\n[![codecov](https://codecov.io/gh/sdss/hal/branch/main/graph/badge.svg)](https://codecov.io/gh/sdss/hal)\n\nHigh-level observing actor for SDSS-V (replaces SOP)\n\n## Installation\n\nYou should be able to install `HAL` by doing\n\n```console\npip install sdss-hal\n```\n\nTo build from source, use\n\n```console\ngit clone git@github.com:sdss/hal\ncd hal\npip install .\n```\n',
    'author': 'José Sánchez-Gallego',
    'author_email': 'gallegoj@uw.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sdss/hal',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
