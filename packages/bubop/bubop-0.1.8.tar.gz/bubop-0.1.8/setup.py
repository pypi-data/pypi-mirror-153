# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bubop']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'loguru>=0.5.3,<0.6.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'bubop',
    'version': '0.1.8',
    'description': "Bergercookie's Useful Bits Of Python",
    'long_description': '# bubop - Bergercookie\'s Useful Bits Of Python\n\n<a href="https://github.com/bergercookie/bubop/actions" alt="CI">\n<img src="https://github.com/bergercookie/bubop/actions/workflows/ci.yml/badge.svg" /></a>\n<a href="https://github.com/pre-commit/pre-commit">\n<img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white" alt="pre-commit"></a>\n\n<a href=\'https://coveralls.io/github/bergercookie/bubop?branch=master\'>\n<img src=\'https://coveralls.io/repos/github/bergercookie/bubop/badge.svg?branch=master\' alt=\'Coverage Status\' /></a>\n<a href="https://github.com/bergercookie/bubop/blob/master/LICENSE.md" alt="LICENSE">\n<img src="https://img.shields.io/github/license/bergercookie/bubop.svg" /></a>\n<a href="https://pypi.org/project/bubop/" alt="pypi">\n<img src="https://img.shields.io/pypi/pyversions/bubop.svg" /></a>\n<a href="https://badge.fury.io/py/bubop">\n<img src="https://badge.fury.io/py/bubop.svg" alt="PyPI version" height="18"></a>\n<a href="https://pepy.tech/project/bubop">\n<img alt="Downloads" src="https://pepy.tech/badge/bubop"></a>\n<a href="https://github.com/psf/black">\n<img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n\n## Description\n\nThis is a collection of python utils that I seem to be re-writing again and\nagain in all new python projects of mine.\n\n## Installation\n\nJust install them with pip:\n\n```sh\npip3 install --user bubop\n\n# Or via poetry:\npoetry add bubop\n```\n',
    'author': 'Nikos Koukis',
    'author_email': 'nickkouk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bergercookie/bubop',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
