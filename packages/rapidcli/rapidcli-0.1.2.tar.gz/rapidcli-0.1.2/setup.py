# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rapidcli',
 'rapidcli.rapid_admin',
 'rapidcli.rapid_admin.admin',
 'rapidcli.tests']

package_data = \
{'': ['*'],
 'rapidcli.rapid_admin': ['templates/rapidcli_app_template/*',
                          'templates/rapidcli_cli_template/*']}

install_requires = \
['GitPython>=3.1.27,<4.0.0',
 'Jinja2>=3.1.2,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'pandas>=1.4.2,<2.0.0',
 'protobuf>=4.21.1,<5.0.0',
 'tqdm>=4.64.0,<5.0.0']

entry_points = \
{'console_scripts': ['rapidcli = rapidcli.rapid_admin.rapid_admin:main']}

setup_kwargs = {
    'name': 'rapidcli',
    'version': '0.1.2',
    'description': 'A rapid CLI framework meant for developers who need complex solutions with minimal work.',
    'long_description': None,
    'author': 'benjamin garrard',
    'author_email': 'benjamingarrard5279@gmail.com',
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
