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
    'version': '0.1.0',
    'description': 'A simple CLI pretty .json viewer',
    'long_description': '# Johnson\n\nA pretty .json viewer\n',
    'author': 'sjlva',
    'author_email': 'rafaelsilva@posteo.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
