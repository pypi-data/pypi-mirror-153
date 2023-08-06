# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mondeja_bump']
install_requires = \
['tomlkit>=0.11.0,<0.12.0']

entry_points = \
{'console_scripts': ['bump = mondeja_bump:main']}

setup_kwargs = {
    'name': 'mondeja-bump',
    'version': '0.1.1',
    'description': 'Just bump semantic version.',
    'long_description': "# mondeja's bump\n",
    'author': 'Álvaro Mondéjar Rubio',
    'author_email': 'mondejar1994@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
