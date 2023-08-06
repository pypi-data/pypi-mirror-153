# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['johnson']

package_data = \
{'': ['*']}

install_requires = \
['rich[all]>=12.4.4,<13.0.0', 'typer[all]>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['johnson = johnson.main:app']}

setup_kwargs = {
    'name': 'johnson',
    'version': '0.1.1',
    'description': 'A simple CLI pretty .json viewer',
    'long_description': '# Johnson\n\nA pretty .json viewer\n\n## Where to get it\n\nThe source code is currently hosted on Github at: https://github.com/sjlva/johnson \n\nBinary installers for the latest version are available at the https://pypi.org/project/johnson/ \n\n```bash\npip install jhonson\n```\n\n## Usage\n\n`johnson --help` returns all commands available.\n\n`johnson --file {file.json}` pretty prints on screen the {file.json} file.\n\n`--indent` or `-i` sets the indent level (default is 4 spaces).\n\n`--paging` or `--no-paging` enables / disables paging navigation through file (default is --no-paging). **Note:** Since the default pager on most platforms do not support color. Johnson will strip color from the output.\n',
    'author': 'sjlva',
    'author_email': 'rafaelsilva@posteo.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sjlva/johnson',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
