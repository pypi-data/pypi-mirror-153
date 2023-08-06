# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['connect', 'connect.eaas.core', 'connect.eaas.core.inject']

package_data = \
{'': ['*']}

install_requires = \
['connect-openapi-client>=25.4',
 'fastapi-utils>=0.2.1,<0.3.0',
 'fastapi>=0.78.0,<0.79.0',
 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'connect-eaas-core',
    'version': '2.1.1',
    'description': 'Connect Eaas Core',
    'long_description': '',
    'author': 'CloudBlue LLC',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://connect.cloudblue.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
