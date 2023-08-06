# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['usergen']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.4.2,<2.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'usergen',
    'version': '0.1.1',
    'description': 'A simple cli package to make requests on randomuser api.',
    'long_description': None,
    'author': 'João Nogueira',
    'author_email': 'joaopcnogueira@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
