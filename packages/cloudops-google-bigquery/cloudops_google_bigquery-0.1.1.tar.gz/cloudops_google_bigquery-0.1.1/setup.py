# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cloudops_google_bigquery']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-bigquery>=3.1.0,<4.0.0',
 'pandas-gbq>=0.17.5,<0.18.0',
 'pandas>=1.4.2,<2.0.0']

setup_kwargs = {
    'name': 'cloudops-google-bigquery',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Manuel Castillo',
    'author_email': 'manucalop@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
