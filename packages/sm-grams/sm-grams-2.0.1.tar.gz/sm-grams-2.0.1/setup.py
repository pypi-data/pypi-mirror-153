# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grams',
 'grams.algorithm',
 'grams.algorithm.candidate_graph',
 'grams.algorithm.data_graph',
 'grams.algorithm.deprecated',
 'grams.algorithm.inferences',
 'grams.algorithm.inferences.features',
 'grams.algorithm.literal_matchers',
 'grams.algorithm.postprocessing',
 'grams.html_table_parser',
 'grams.inputs']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'click>=8.1.3,<9.0.0',
 'fastnumbers>=3.1.0,<4.0.0',
 'ftfy>=6.1.1,<7.0.0',
 'graph-wrapper>=1.4.0,<2.0.0',
 'html5lib>=1.1,<2.0',
 'hugedict>=1.4.0,<2.0.0',
 'ipython>=8.0.1,<9.0.0',
 'kgdata>=2.2.1,<3.0.0',
 'loguru>=0.6.0',
 'matplotlib>=3.4.2,<4.0.0',
 'ned>=1.0.0,<2.0.0',
 'networkx>=2.8.2,<3.0.0',
 'omegaconf>=2.0.6,<3.0.0',
 'orjson>=3.6.8,<4.0.0',
 'pslpython>=2.2.2,<3.0.0',
 'python-Levenshtein>=0.12.2,<0.13.0',
 'python-slugify>=5.0.2,<6.0.0',
 'rdflib>=6.1.1,<7.0.0',
 'requests>=2.27.1,<3.0.0',
 'rltk==2.0.0-alpha.15',
 'ruamel.yaml>=0.17.9,<0.18.0',
 'sem-desc>=3.5.1,<3.6.0',
 'steiner-tree>=1.1.3,<2.0.0',
 'tqdm>=4.64.0,<5.0.0',
 'typing_extensions>=4.0.0,<5.0.0',
 'ujson>=5.1.0,<6.0.0']

entry_points = \
{'console_scripts': ['grams = grams.cli:cli']}

setup_kwargs = {
    'name': 'sm-grams',
    'version': '2.0.1',
    'description': '',
    'long_description': '<h1 align="center">GRAMS</h1>\n\n<div align="center">\n\n![PyPI](https://img.shields.io/pypi/v/sm-grams)\n![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)\n[![GitHub Issues](https://img.shields.io/github/issues/usc-isi-i2/GRAMS.svg)](https://github.com/usc-isi-i2/GRAMS/issues)\n![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)\n[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)\n\n</div>\n\n## Table of Contents\n- [Introduction](#introduction)\n- [Installation](#installation)\n<!-- - [Example](#example)\n- [Contributing](#contributing)\n<!-- - [Support](#support) -->\n\n## Introduction\n\nGRAMS is a library to build semantic descriptions of tables to map them to Wikidata.\n\n## Installation\n\nPlease look in the [wiki](https://github.com/usc-isi-i2/grams/wiki/Installation) for how to install GRAMS\n',
    'author': 'Binh Vu',
    'author_email': 'binh@toan2.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/usc-isi-i2/grams',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
