# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['severino',
 'severino.sdk',
 'severino.sdk.airflow',
 'severino.sdk.helpers',
 'severino.sdk.internal_recruitment',
 'severino.sdk.reports_of_pcds_in_admission',
 'severino.sdk.rescission_workflow',
 'severino.sdk.store_data',
 'severino.sdk.vagas_dot_com']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'severino',
    'version': '0.3.0',
    'description': 'O Severino é utilizado para facilitar as integrações e também a reutilização de código',
    'long_description': None,
    'author': 'Stone People Analytics',
    'author_email': 'systems-techpeople@stone.com.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
