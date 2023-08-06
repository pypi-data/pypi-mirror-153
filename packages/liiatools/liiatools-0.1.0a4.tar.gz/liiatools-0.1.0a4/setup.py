# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['liiatools',
 'liiatools.datasets',
 'liiatools.datasets.annex_a',
 'liiatools.datasets.annex_a.lds_annexa_clean',
 'liiatools.datasets.shared_functions',
 'liiatools.spec',
 'liiatools.spec.annex_a',
 'liiatools.tests',
 'liiatools.util']

package_data = \
{'': ['*'], 'liiatools.spec': ['annex_a/samples/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'XlsxWriter>=3.0.3,<4.0.0',
 'click-log>=0.4.0,<0.5.0',
 'click>=8.1.2,<9.0.0',
 'dacite>=1.6.0,<2.0.0',
 'lxml>=4.8.0,<5.0.0',
 'more-itertools>=8.12.0,<9.0.0',
 'openpyxl>=3.0.9,<4.0.0',
 'pandas>=1.4.2,<2.0.0',
 'regex>=2022.4.24,<2023.0.0',
 'sfdata-stream-parser==0.4.1',
 'tablib[cli,xlsx]>=3.2.0,<4.0.0',
 'xlrd>=2.0.1,<3.0.0',
 'xmlschema>=1.10.0,<2.0.0']

setup_kwargs = {
    'name': 'liiatools',
    'version': '0.1.0a4',
    'description': "Children's Services Data Tools - Utilities for cleaning and normalising CS data by Social Finance",
    'long_description': None,
    'author': 'Michael Hanks',
    'author_email': 'michael.hanks@socialfinance.org.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
