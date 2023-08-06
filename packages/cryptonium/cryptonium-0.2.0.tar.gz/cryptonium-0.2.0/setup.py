# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cryptonium']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=36.0.0,<38.0.0']

setup_kwargs = {
    'name': 'cryptonium',
    'version': '0.2.0',
    'description': 'Crypto library',
    'long_description': '===========================\ncryptonium: Crypto library\n===========================\n\n.. image:: https://github.com/piper-hq/cryptonium/actions/workflows/build.yml/badge.svg\n  :alt: Build\n  :target: https://github.com/piper-hq/cryptonium/actions/workflows/build.yml\n.. image:: https://img.shields.io/lgtm/alerts/g/piper-hq/cryptonium.svg\n  :alt: Total alerts\n  :target: https://lgtm.com/projects/g/piper-hq/cryptonium/alerts/\n.. image:: https://img.shields.io/github/license/piper-hq/cryptonium\n  :alt: License\n  :target: https://github.com/piper-hq/cryptonium/blob/main/LICENSE.txt\n.. image:: https://img.shields.io/pypi/v/cryptonium\n  :alt: PyPI\n  :target: https://pypi.org/project/cryptonium\n.. image:: https://pepy.tech/badge/cryptonium\n  :alt: Downloads\n  :target: https://pepy.tech/project/cryptonium\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n  :alt: Code style\n  :target: https://github.com/psf/black\n\n``cryptonium`` offers an easy interface to encrypt/decrypt strings and files.\n\nIn a nutshell\n-------------\n\nInstallation\n^^^^^^^^^^^^\n\nThe easiest way is to use `poetry`_ to manage your dependencies and add *cryptonium* to them.\n\n.. code-block:: toml\n\n    [tool.poetry.dependencies]\n    cryptonium = "^0.2.0"\n\nUsage\n^^^^^\n\nA class called SymmetricCrypto for encrypting and decrypting strings and files is available.\n\nLinks\n-----\n\n- `Documentation`_\n- `Changelog`_\n\n\n.. _poetry: https://python-poetry.org/\n.. _Changelog: https://github.com/piper-hq/cryptonium/blob/main/CHANGELOG.rst\n.. _Documentation: https://cryptonium.readthedocs.io/en/latest/\n',
    'author': 'PiperHQ',
    'author_email': 'tech@piperhq.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/piper-hq/cryptonium',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
