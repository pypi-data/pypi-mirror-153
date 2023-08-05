# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spectral_metric']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.1.0,<2.0.0',
 'matplotlib>=3.5.0,<4.0.0',
 'scikit-learn>=1.0.1,<2.0.0',
 'seaborn>=0.11.2,<0.12.0']

setup_kwargs = {
    'name': 'spectral-metric',
    'version': '0.6.0',
    'description': 'Implementation of Cumulative Spectral Gradient (CSG), a measure to estimate the complexity of datasets. This works has been presented at CVPR 2019.',
    'long_description': None,
    'author': 'Dref360',
    'author_email': 'frederic.branchaud.charron@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
