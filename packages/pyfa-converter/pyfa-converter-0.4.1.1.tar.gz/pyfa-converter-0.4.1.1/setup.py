# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfa_converter']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.75.1,<0.76.0',
 'pydantic>=1.9.0,<2.0.0',
 'python-multipart>=0.0.5,<0.0.6']

setup_kwargs = {
    'name': 'pyfa-converter',
    'version': '0.4.1.1',
    'description': 'Pydantic to fastapi model converter.',
    'long_description': None,
    'author': 'dotX12',
    'author_email': 'dev@shitposting.team',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
