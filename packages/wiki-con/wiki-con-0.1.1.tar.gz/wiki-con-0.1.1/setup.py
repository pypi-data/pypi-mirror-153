# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wiki_con']

package_data = \
{'': ['*']}

install_requires = \
['Pygments>=2.12.0,<3.0.0',
 'click>=8.1.3,<9.0.0',
 'desert>=2020.11.18,<2021.0.0',
 'marshmallow>=3.16.0,<4.0.0',
 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['wiki_con = wiki_con.console:main']}

setup_kwargs = {
    'name': 'wiki-con',
    'version': '0.1.1',
    'description': 'A hypermodern Python project',
    'long_description': '## wiki-con - A console app that displays random facts using the Wikipedia API\n\n[![Tests](https://github.com/kevinbowen777/wiki-con/workflows/Tests/badge.svg)](https://github.com/kevinbowen777/wiki-con/actions?workflow=Tests)\n\n### Installation\n - `git clone https://github.com/kevinbowen777/wiki-con.git`\n - `cd wiki-con`\n - `poetry run wiki_con`\n\n---\n## Features\n - TBD\n\n---\n[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/kevinbowen777/wiki-con/blob/master/LICENSE)\n---\n### Reporting Bugs\n\n   Visit the [Issues page](https://github.com/kevinbowen777/wiki-con/issues) to view currently open bug reports or open a new issue.\n',
    'author': 'Kevin Bowen',
    'author_email': 'kevin.bowen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kevinbowen777/wiki-con/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
