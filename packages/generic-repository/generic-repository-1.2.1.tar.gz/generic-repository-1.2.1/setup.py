# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['generic_repository']

package_data = \
{'': ['*']}

modules = \
['py']
extras_require = \
{':python_version < "3.10"': ['typing-extensions>=4.2.0,<5.0.0'],
 ':python_version < "3.8"': ['cached-property>=1.5.2,<2.0.0'],
 'http': ['httpx>=0.23.0,<0.24.0'],
 'pydantic': ['pydantic>=1.9.0,<2.0.0'],
 'sqlalchemy': ['SQLAlchemy>=1.4.0,<2.0.0']}

setup_kwargs = {
    'name': 'generic-repository',
    'version': '1.2.1',
    'description': 'Generic repository patterm for python.',
    'long_description': '# Generic repository\n\n[![Coverage Status for dev branch](https://coveralls.io/repos/github/francipvb/generic-repository/badge.svg?branch=develop)](https://coveralls.io/github/francipvb/generic-repository?branch=develop)\n[![Coverage Status for main branch](https://coveralls.io/repos/github/francipvb/generic-repository/badge.svg?branch=main)](https://coveralls.io/github/francipvb/generic-repository?branch=main)\n\nThis package includes building blocks to apply repository pattern in your program.\n\n## Usage\n\nFor extensive usage examples, please see the tests.\n\nDocumentation about all kind of repository implementations will be added later.\n',
    'author': 'Francisco Del Roio',
    'author_email': 'francipvb@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
