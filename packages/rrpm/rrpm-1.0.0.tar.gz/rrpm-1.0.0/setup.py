# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rrpm']

package_data = \
{'': ['*']}

install_requires = \
['questionary>=1.10.0,<2.0.0',
 'rich>=12.4.4,<13.0.0',
 'toml>=0.10.2,<0.11.0',
 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['pm = rrpm.rrpm:cli']}

setup_kwargs = {
    'name': 'rrpm',
    'version': '1.0.0',
    'description': 'A tool to manage all your projects easily!',
    'long_description': None,
    'author': 'pybash1',
    'author_email': 'example@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
