# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdut']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'click>=8.1.3,<9.0.0',
 'httpx>=0.23.0,<0.24.0',
 'pyperclip>=1.8.2,<2.0.0']

entry_points = \
{'console_scripts': ['mdut = mdut.mdut:mdut']}

setup_kwargs = {
    'name': 'mdut',
    'version': '22.6.0',
    'description': 'Markdown URL tag generator',
    'long_description': '# mdut\n\n**mdut** (pronounced "em-doot") is a tool for generating Markdown URL tags.\nIt ships as both a standalone command-line program and Python library.\n\n[![GitHub Actions](https://github.com/nkantar/mdut/actions/workflows/automated_checks.yml/badge.svg?branch=main)](https://github.com/nkantar/mdut/actions/workflows/code-quality-checks.yml)\n[![PyPI version](https://badge.fury.io/py/mdut.svg)](https://badge.fury.io/py/mdut)\n[![Unreleased changes](https://img.shields.io/github/commits-since/nkantar/mdut/22.6.0)](https://github.com/nkantar/mdut/blob/main/CHANGELOG.md#unreleased)\n[![License: MIT](https://img.shields.io/github/license/nkantar/mdut)](https://github.com/nkantar/mdut/blob/main/LICENSE)\n\n\n## Examples\n\nCommand-line program:\n\n```\n# reference style is default\n$ mdut https://example.com\nCopied to clipboard:\n[TODO]: https://example.com "Example Domain"\n\n$ mdut -s inline https://example.com\nCopied to clipboard:\n[TODO](https://example.com "Example Domain")\n\n$ mdut -s slack https://example.com\nCopied to clipboard:\n[TODO](https://example.com)\n```\n\nPython library:\n\n```python\n>>> import mdut\n>>> mdut.reference("https://example.com")\n\'[TODO]: https://example.com "Example Domain"\'\n>>> mdut.inline("https://example.com")\n\'[TODO](https://example.com "Example Domain")\'\n>>> mdut.slack("https://example.com")\n\'[TODO](https://example.com)\'\n```\n\n\n## Installation\n\nIf you plan on using mdut on the command-line, you\'re probably best off installing it via [pipx], like so:\n\n```\npipx install mdut\n```\n\nHowever, if you plan on using mdut as a library in your project, you should probably install it the same way as your other dependencies, for example via pip, Poetry, Pipenv, etc.\n\n```\n# pip\npip install mdut\n\n# Poetry\npoetry add mdut\n\n# Pipenv\npipenv install mdut\n```\n\n\n[pipx]: https://pypa.github.io/pipx/ "pipx"\n',
    'author': 'Nik Kantar',
    'author_email': 'nik@nkantar.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nkantar/mdut',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
