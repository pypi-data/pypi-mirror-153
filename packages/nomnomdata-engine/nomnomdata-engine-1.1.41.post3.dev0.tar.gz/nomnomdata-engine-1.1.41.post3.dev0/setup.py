# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nomnomdata', 'nomnomdata.engine']

package_data = \
{'': ['*']}

install_requires = \
['dunamai>=1.1.0,<2.0.0',
 'httmock>=1.3.0,<2.0.0',
 'nomnomdata-cli>=0.1.7,<0.2.0',
 'pyyaml>=5.3.1,<6.0.0',
 'requests>=2.23.0,<3.0.0',
 'wrapt>=1.12.1,<2.0.0']

setup_kwargs = {
    'name': 'nomnomdata-engine',
    'version': '1.1.41.post3.dev0',
    'description': 'Package containing tooling for developing nominode engines',
    'long_description': 'Package for developing nominode engines\n',
    'author': 'Nom Nom Data Inc',
    'author_email': 'info@nomnomdata.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/nomnomdata/tools/nomnomdata-engine',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
