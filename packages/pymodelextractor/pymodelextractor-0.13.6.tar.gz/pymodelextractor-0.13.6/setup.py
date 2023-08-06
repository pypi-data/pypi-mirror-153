# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymodelextractor',
 'pymodelextractor.exceptions',
 'pymodelextractor.learners',
 'pymodelextractor.learners.observation_table_learners',
 'pymodelextractor.learners.observation_table_learners.translators',
 'pymodelextractor.learners.observation_tree_learners',
 'pymodelextractor.teachers',
 'pymodelextractor.tests',
 'pymodelextractor.tests.learners_tests',
 'pymodelextractor.utils']

package_data = \
{'': ['*']}

install_requires = \
['pythautomata>=0.19.4,<0.20.0']

setup_kwargs = {
    'name': 'pymodelextractor',
    'version': '0.13.6',
    'description': '',
    'long_description': None,
    'author': 'Federico VIlensky',
    'author_email': 'fedevilensky@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
