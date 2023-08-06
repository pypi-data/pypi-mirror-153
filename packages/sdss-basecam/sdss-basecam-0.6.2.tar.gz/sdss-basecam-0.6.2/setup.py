# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['basecam', 'basecam.actor', 'basecam.actor.commands', 'basecam.models']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.17,<2.0', 'sdss-clu>=1.6.0,<2.0.0', 'sdsstools>=0.4.0']

extras_require = \
{':python_version <= "3.7"': ['typing-extensions>=3.7.4,<4.0.0'],
 ':python_version >= "3.10"': ['astropy>=5.0,<6.0'],
 ':python_version >= "3.7" and python_version < "3.10"': ['astropy>=4.2,<5.0']}

setup_kwargs = {
    'name': 'sdss-basecam',
    'version': '0.6.2',
    'description': 'A base library for camera wrapping and actor.',
    'long_description': 'basecam\n=======\n\n![Versions](https://img.shields.io/badge/python-3.8-blue)\n[![PyPI version](https://badge.fury.io/py/sdss-basecam.svg)](https://badge.fury.io/py/sdss-basecam)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Documentation Status](https://readthedocs.org/projects/sdss-basecam/badge/?version=latest)](https://sdss-basecam.readthedocs.io/en/latest/?badge=latest)\n[![Build](https://img.shields.io/github/workflow/status/sdss/basecam/Test)](https://github.com/sdss/basecam/actions)\n[![Coverage Status](https://codecov.io/gh/sdss/basecam/branch/master/graph/badge.svg)](https://codecov.io/gh/sdss/basecam)\n\n``basecam`` provides a wrapper around CCD camera APIs with an SDSS-style TCP/IP actor. The main benefits of using `basecam` are:\n\n- Simplifies the creation of production-level camera libraries by providing all the common boilerplate so that you only need to focus on implementing the parts that are specific to your camera API.\n- Provides a common API regardless of the underlying camera being handled.\n- Powerful event handling and notification.\n',
    'author': 'José Sánchez-Gallego',
    'author_email': 'gallegoj@uw.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sdss/basecam',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
