# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['leximpact_aggregates']

package_data = \
{'': ['*']}

install_requires = \
['StrEnum>=0.4.7,<0.5.0',
 'dataclasses-json>=0.5.7,<0.6.0',
 'leximpact-socio-fisca-simu-etat>=0.1.4,<0.2.0',
 'matplotlib>=3.5.1,<4.0.0',
 'nbdev>=1.2.2,<2.0.0',
 'openpyxl>=3.0.9,<4.0.0',
 'pre-commit>=2.17.0,<3.0.0',
 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'leximpact-aggregates',
    'version': '0.0.9',
    'description': 'Store aggregates of french data.',
    'long_description': None,
    'author': 'LexImpact',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
