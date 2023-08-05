# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['synthesis',
 'synthesis.evaluation',
 'synthesis.synthesizers',
 'synthesis.transformers']

package_data = \
{'': ['*']}

install_requires = \
['diffprivlib==0.5.1',
 'dill>=0.3.4,<0.4.0',
 'dython>=0.6.7,<0.7.0',
 'joblib>=1.0.1,<2.0.0',
 'lifelines>=0.26.0,<0.27.0',
 'matplotlib>=3.4.3,<4.0.0',
 'numpy>=1.21.2,<2.0.0',
 'pandas>=1.3.2,<2.0.0',
 'pip>=22.1.1,<23.0.0',
 'pyjanitor>=0.21.2,<0.22.0',
 'scikit-learn==1.0.2',
 'scipy>=1.7.1,<2.0.0',
 'seaborn>=0.11.2,<0.12.0',
 'thomas-core>=0.1.3,<0.2.0']

setup_kwargs = {
    'name': 'synthetic-data-generation',
    'version': '0.1.6',
    'description': 'Algorithms for generating synthetic data',
    'long_description': None,
    'author': 'Daan Knoors',
    'author_email': 'd.knoors@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
