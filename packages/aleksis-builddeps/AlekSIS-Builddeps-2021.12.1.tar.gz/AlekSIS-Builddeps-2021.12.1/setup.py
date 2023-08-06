# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['aleksis_builddeps']
install_requires = \
['black>=21.0',
 'curlylint>=0.13.0,<0.14.0',
 'django-stubs>=1.1,<2.0',
 'flake8-bandit>=3.0.0,<4.0.0',
 'flake8-black>=0.3.0,<0.4.0',
 'flake8-builtins>=1.4.1,<2.0.0',
 'flake8-django>=1.0.0,<2.0.0',
 'flake8-docstrings>=1.5.0,<2.0.0',
 'flake8-fixme>=1.1.1,<2.0.0',
 'flake8-isort>=4.0.0,<5.0.0',
 'flake8-mypy>=17.8.0,<18.0.0',
 'flake8-rst-docstrings>=0.2.0,<0.3.0',
 'flake8>=4.0.0,<5.0.0',
 'freezegun>=1.1.0,<2.0.0',
 'isort>=5.0.0,<6.0.0',
 'pytest-cov>=3.0.0,<4.0.0',
 'pytest-django-testing-postgresql>=0.2,<0.3',
 'pytest-django>=4.1,<5.0',
 'pytest-sugar>=0.9.2,<0.10.0',
 'pytest>=6.0,<7.0',
 'safety>=1.8.5,<2.0.0',
 'selenium>=4.0.0,<5.0.0',
 'sphinx-autodoc-typehints>=1.7,<2.0',
 'sphinx>=3.0,<4.0',
 'sphinx_material>=0.0.35,<0.0.36',
 'sphinxcontrib-django>=0.5.0,<0.6.0',
 'sphinxcontrib-svg2pdfconverter>=1.1.1,<2.0.0']

setup_kwargs = {
    'name': 'aleksis-builddeps',
    'version': '2021.12.1',
    'description': 'AlekSIS (School Information System)\u200a—\u200aBuild/Dev dependencies for apps',
    'long_description': None,
    'author': 'Dominik George',
    'author_email': 'dominik.george@teckids.org',
    'maintainer': 'Jonathan Weth',
    'maintainer_email': 'wethjo@katharineum.de',
    'url': 'https://aleksis.org/',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
