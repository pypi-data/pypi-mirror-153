# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sm',
 'sm.evaluation',
 'sm.inputs',
 'sm.misc',
 'sm.misc.graph',
 'sm.namespaces',
 'sm.outputs']

package_data = \
{'': ['*'], 'sm': ['data/*']}

install_requires = \
['chardet>=4.0.0,<5.0.0',
 'colorama>=0.4.4',
 'graph-wrapper>=1.4.0,<2.0.0',
 'ipython>=8.0.1,<9.0.0',
 'lbry-rocksdb-optimized>=0.8.1,<0.9.0',
 'loguru>=0.6.0',
 'matplotlib>=3.4.2,<4.0.0',
 'orjson>=3.6.8,<4.0.0',
 'pandas>=1.4.1,<2.0.0',
 'pydot>=1.4.2,<2.0.0',
 'pyrsistent>=0.17.3,<0.18.0',
 'python-slugify>=5.0.2,<6.0.0',
 'rdflib>=6.1.1,<7.0.0',
 'ruamel.yaml>=0.17.9,<0.18.0',
 'tqdm>=4.64.0,<5.0.0',
 'ujson>=5.1.0,<6.0.0']

setup_kwargs = {
    'name': 'sem-desc',
    'version': '3.5.1',
    'description': 'Package providing basic functionalities for the semantic modeling problem',
    'long_description': 'Containing basic functions (input, output, evaluation metrics) for the semantic modeling problem.\n',
    'author': 'Binh Vu',
    'author_email': 'binh@toan2.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/binh-vu/sm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
