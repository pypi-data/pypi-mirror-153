# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['flake8_complicated_walrus']
install_requires = \
['astpretty>=2.1.0,<3.0.0', 'flake8>=4,<5']

entry_points = \
{'flake8.extension': ['FCW = flake8_complicated_walrus:Plugin']}

setup_kwargs = {
    'name': 'flake8-complicated-walrus',
    'version': '1.0.1',
    'description': 'This Flake8 plugin for checking complicated assignment expressions.',
    'long_description': '# flake8-complicated-walrus\n\nThis *Flake8* plugin for checking complicated assignment expressions.\nThere are 3 levels for this linter:\n1. *restrict-all* - **restrict** use assignment expressions **in any case**\n2. *restrict-complicated* - **restrict** use assignment expressions **in complex if conditions**\n3. *allow-all* - **allow** use assignment expressions **in any case**\n\n# Quick Start Guide\n\n1. Install ``flake8-complicated-walrus`` from PyPI with pip::\n\n        pip install flake8-complicated-walrus\n\n2. Configure a mark that you would like to validate::\n\n        cd project_root/\n        vi setup.cfg\n\n3. Add to file following: \n   \n        [flake8]  \n        restrict-walrus-level = restrict-complicated  \n\n3. Run flake8::\n\n        flake8 .\n\n# flake8 codes\n\n   * FCW100: You cannot use assignment expression.\n   * FCW200: You cannot use assignment expression in complicated if statements.\n\n# Settings\n\n**restrict-walrus-level**  \nIt specifies restrict level for linting your code. \n',
    'author': 'Dudov Dmitry',
    'author_email': 'dudov.dm@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DDmitiy/flake8-complicated-walrus',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
