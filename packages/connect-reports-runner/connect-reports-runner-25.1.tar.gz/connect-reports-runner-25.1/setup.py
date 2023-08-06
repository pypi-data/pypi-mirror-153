# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['executor']

package_data = \
{'': ['*']}

install_requires = \
['chardet>=3.0.0,<4.0.0',
 'connect-openapi-client>=25.3',
 'connect-reports-core>=24.0.0,<25.0.0',
 'lxml>=4.0.0,<5.0.0',
 'openpyxl>=3.0.0,<4.0.0',
 'requests>=2.0.0,<3.0.0']

entry_points = \
{'console_scripts': ['cextrun = executor.runner:run_executor']}

setup_kwargs = {
    'name': 'connect-reports-runner',
    'version': '25.1',
    'description': 'Connect Reports Runner',
    'long_description': 'Connect Reports Executor\n========================\n\nThis project contains the executor code used to run custom reports on CloudBlue Connect.\n',
    'author': 'CloudBlue LLC',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://connect.cloudblue.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
