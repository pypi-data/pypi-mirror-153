# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libtable']

package_data = \
{'': ['*']}

install_requires = \
['prompt-toolkit>=3.0.29,<4.0.0']

setup_kwargs = {
    'name': 'libtable',
    'version': '0.2.0',
    'description': 'Python library for cli tables',
    'long_description': '# Welcome to libtable\n\n[![](https://badgen.net/github/release/sguerri/libtable)](https://github.com/sguerri/libtable/releases/)\n[![](https://img.shields.io/github/workflow/status/sguerri/libtable/Build/v0.2.0)](https://github.com/sguerri/libtable/actions/workflows/build.yml)\n[![](https://badgen.net/github/license/sguerri/libtable)](https://www.gnu.org/licenses/)\n[![](https://badgen.net/pypi/v/libtable)](https://pypi.org/project/libtable/)\n[![](https://badgen.net/pypi/python/libtable)](#)\n[![](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)](#)\n\n> Python library for cli tables\n\nWork in Progress\n\n**Main features**\n* TODO\n\n**Roadmap**\n* TODO\n\n---\n\n- [Welcome to libtable](#welcome-to-libtable)\n  * [Installation](#installation)\n  * [Usage](#usage)\n  * [Build](#build)\n  * [Dependencies](#dependencies)\n  * [Author](#author)\n  * [Issues](#issues)\n  * [License](#license)\n\n## Installation\n\nTODO\n\n## Usage\n\nTODO\n\n## Build\n\nTODO\n\n## Dependencies\n\n**Python Libraries**\n- [python-prompt-toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit)\n\n**Python Development Libraries**\n- [poetry](https://python-poetry.org/)\n\n## Author\n\nSébastien Guerri - [github page](https://github.com/sguerri)\n\n## Issues\n\nContributions, issues and feature requests are welcome!\n\nFeel free to check [issues page](https://github.com/sguerri/libtable/issues). You can also contact me.\n\n## License\n\nCopyright (C) 2022 Sebastien Guerri\n\nlibtable is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.\n\nlibtable is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License along with libtable. If not, see <https://www.gnu.org/licenses/>.',
    'author': 'Sebastien GUERRI',
    'author_email': 'nierrgu@bmel.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sguerri/libtable',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
