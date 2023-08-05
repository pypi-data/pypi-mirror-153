# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geomeffibem', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.2,<4.0.0',
 'numpy>=1.22.4,<2.0.0',
 'openstudio==3.4.0',
 'pandas>=1.4.2,<2.0.0']

extras_require = \
{'dev': ['tox>=3.25.0,<4.0.0',
         'virtualenv>=20.14.1,<21.0.0',
         'pip>=22.1.1,<23.0.0',
         'twine>=4.0.0,<5.0.0',
         'pre-commit>=2.19.0,<3.0.0',
         'toml>=0.10.2,<0.11.0',
         'bump2version>=1.0.1,<2.0.0'],
 'doc': ['mkdocs>=1.3.0,<2.0.0',
         'mkdocs-include-markdown-plugin>=3.5.1,<4.0.0',
         'mkdocs-material>=8.2.16,<9.0.0',
         'mkdocstrings>=0.19.0,<0.20.0',
         'mkdocstrings-python>=0.7.0,<0.8.0',
         'mkdocs-autorefs>=0.4.1,<0.5.0'],
 'test': ['black>=22.3.0,<23.0.0',
          'isort>=5.10.1,<6.0.0',
          'flake8>=4.0.1,<5.0.0',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'mypy>=0.960,<0.961',
          'pytest>=7.1.2,<8.0.0',
          'pytest-cov>=3.0.0,<4.0.0']}

setup_kwargs = {
    'name': 'geomeffibem',
    'version': '0.1.1',
    'description': 'A small library to facilitate some building energy modeling geometry operations with OpenStudio and EnergyPlus in mind.',
    'long_description': '# GeomEffiBEM\n\n\n[![pypi](https://img.shields.io/pypi/v/geomeffibem.svg)](https://pypi.org/project/geomeffibem/)\n[![python](https://img.shields.io/pypi/pyversions/geomeffibem.svg)](https://pypi.org/project/geomeffibem/)\n[![Build Status](https://github.com/jmarrec/geomeffibem/actions/workflows/dev.yml/badge.svg)](https://github.com/jmarrec/geomeffibem/actions/workflows/dev.yml)\n[![codecov](https://codecov.io/gh/jmarrec/geomeffibem/branch/main/graphs/badge.svg)](https://codecov.io/github/jmarrec/geomeffibem)\n\n\nA small library to facilitate some building energy modeling geometry operations with OpenStudio and EnergyPlus in mind\n\nA Jupyter Notebook[GeoEffiBEM_Demonstration.ipynb](GeomEffiBEM_Demonstation.ipynb) can serve as a small demonstration of the features.\n\n\n* Documentation: <https://jmarrec.github.io/geomeffibem>\n* GitHub: <https://github.com/jmarrec/geomeffibem>\n* PyPI: <https://pypi.org/project/geomeffibem/>\n* Free software: MIT\n',
    'author': 'Julien Marrec',
    'author_email': 'contact@effibem.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jmarrec/geomeffibem',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
