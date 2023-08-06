# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nprompter']

package_data = \
{'': ['*'], 'nprompter': ['templates/*', 'web/*']}

install_requires = \
['Jinja2>=3.0.1,<4.0.0',
 'python-dotenv>=0.19.0,<0.20.0',
 'python-slugify>=5.0.2,<6.0.0',
 'requests>=2.26.0,<3.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['nprompter = nprompter.__main__:app']}

setup_kwargs = {
    'name': 'nprompter',
    'version': '1.2.0',
    'description': '',
    'long_description': None,
    'author': 'Antonio Feregrino',
    'author_email': 'antonio.feregrino@gmail.com',
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
