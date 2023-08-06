# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['transmission_rpc']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0', 'typing_extensions>=3.7.4.2,<5.0.0.0']

extras_require = \
{'docs': ['sphinx==4.3.2', 'sphinx-rtd-theme==1.0.0']}

setup_kwargs = {
    'name': 'transmission-rpc',
    'version': '3.3.2',
    'description': 'Python module that implements the Transmission bittorent client JSON-RPC protocol',
    'long_description': '# Transmission-rpc Readme\n\n[![PyPI](https://img.shields.io/pypi/v/transmission-rpc)](https://pypi.org/project/transmission-rpc/)\n[![Documentation Status](https://readthedocs.org/projects/transmission-rpc/badge/)](https://transmission-rpc.readthedocs.io/)\n[![ci](https://github.com/Trim21/transmission-rpc/workflows/ci/badge.svg)](https://github.com/Trim21/transmission-rpc/actions)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/transmission-rpc)](https://pypi.org/project/transmission-rpc/)\n[![Codecov branch](https://img.shields.io/codecov/c/github/Trim21/transmission-rpc/master)](https://codecov.io/gh/Trim21/transmission-rpc/branch/master)\n\n`transmission-rpc` is hosted by GitHub at [github.com/Trim21/transmission-rpc](https://github.com/Trim21/transmission-rpc)\n\n## Introduction\n\n`transmission-rpc` is a python module implementing the json-rpc client protocol for the BitTorrent client Transmission.\n\nSupport rpc version <= 16 (transmission <= 3.00),\nshould works fine with newer rpc version but some new feature may be missing.\n\n## versioning\n\n`transmission-rpc` follow [Semantic Versioning](https://semver.org/),\nreport an issue if you found unexpected API break changes at same major version.\n\n## Install\n\n```console\npip install transmission-rpc -U\n```\n\n## Documents\n\n<https://transmission-rpc.readthedocs.io/>\n\n## Developer\n\n`transmission-rpc` is licensed under the MIT license.\n',
    'author': 'Trim21',
    'author_email': 'i@trim21.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Trim21/transmission-rpc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
