# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scatrex',
 'scatrex.models',
 'scatrex.models.cna',
 'scatrex.ntssb',
 'scatrex.plotting']

package_data = \
{'': ['*']}

install_requires = \
['anndata>=0.7.5,<0.8.0',
 'graphviz>=0.14.1,<0.15.0',
 'gseapy>=0.10.5,<0.11.0',
 'jax==0.2.20',
 'jaxlib==0.1.71',
 'networkx>=2.6.2,<3.0.0',
 'numpy>=1.21.2,<2.0.0',
 'pandas>=1.3.2,<2.0.0',
 'pybiomart>=0.2.0,<0.3.0',
 'pygraphviz>=1.7,<2.0',
 'scanpy>=1.7.0,<2.0.0',
 'scikit-learn>=0.23.2,<0.24.0',
 'scipy>=1.7.3,<2.0.0',
 'tqdm>=4.57.0,<5.0.0']

setup_kwargs = {
    'name': 'scatrex',
    'version': '0.1.1',
    'description': 'Map single-cell transcriptomes to copy number evolutionary trees.',
    'long_description': '<div align="left">\n  <img src="https://github.com/cbg-ethz/SCATrEx/raw/main/figures/scatrex.png", width="300px">\n</div>\n<p></p>\n\n[![PyPI](https://img.shields.io/pypi/v/scatrex.svg?style=flat)](https://pypi.python.org/pypi/scatrex)\n[![Build](https://github.com/cbg-ethz/SCATrEx/actions/workflows/main.yaml/badge.svg)](https://github.com/cbg-ethz/SCATrEx/actions/workflows/main.yaml)\n\n\nMap single-cell transcriptomes to copy number evolutionary trees. Check out the [tutorial](https://github.com/cbg-ethz/SCATrEx/blob/main/notebooks/tutorial.ipynb) for more information.\n\n## Installation\n```\n$ pip install scatrex\n```\n\nSCATrEx uses [JAX](https://github.com/google/jax) to perform automatic differentiation. By default, SCATrEx installs the CPU-only version of JAX, but we strongly recommend the use of GPU acceleration. Please follow the instructions in https://github.com/google/jax#pip-installation-gpu-cuda to install the GPU version of JAX.\n\n## Preprint\nhttps://doi.org/10.1101/2021.11.04.467244\n',
    'author': 'pedrofale',
    'author_email': 'pedro.miguel.ferreira.pf@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cbg-ethz/SCATrEx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
