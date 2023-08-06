# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ui_components']

package_data = \
{'': ['*'], 'ui_components': ['js/*', 'styles/*']}

install_requires = \
['cssselect>=1.1.0,<2.0.0',
 'dominate>=2.6.0,<3.0.0',
 'lxml>=4.9.0,<5.0.0',
 'pydantic>=1.9.1,<2.0.0',
 'ready-logger>=0.1.4,<0.2.0']

setup_kwargs = {
    'name': 'ui-components',
    'version': '0.2.4',
    'description': '',
    'long_description': None,
    'author': 'Dan',
    'author_email': 'kelleherjdan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
