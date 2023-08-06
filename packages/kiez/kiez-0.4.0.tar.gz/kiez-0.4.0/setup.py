# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kiez',
 'kiez.analysis',
 'kiez.evaluate',
 'kiez.hubness_reduction',
 'kiez.io',
 'kiez.neighbors',
 'kiez.neighbors.approximate',
 'kiez.neighbors.exact',
 'kiez.utils']

package_data = \
{'': ['*']}

install_requires = \
['class-resolver>=0.1.0,<0.2.0',
 'joblib>=1.0.0,<2.0.0',
 'numpy>=1.21.0,<2.0.0',
 'pandas>=1.1.5,<2.0.0',
 'scikit-learn>=0.24.1',
 'scipy>=1.3.2,<2.0.0',
 'tqdm>=4.62.3,<5.0.0']

extras_require = \
{'all': ['ngt>=1.8',
         'annoy>=1.17.0,<2.0.0',
         'nmslib>=2.1.1,<3.0.0',
         'faiss-cpu>=1.7.1,<2.0.0',
         'autofaiss>=2.4.0,<3.0.0',
         'faiss-gpu>=1.7.1,<2.0.0'],
 'annoy': ['annoy>=1.17.0,<2.0.0'],
 'docs': ['Sphinx>=5.0.0,<6.0.0', 'insegel>=1.3.1,<2.0.0'],
 'faiss-cpu': ['faiss-cpu>=1.7.1,<2.0.0', 'autofaiss>=2.4.0,<3.0.0'],
 'faiss-gpu': ['autofaiss>=2.4.0,<3.0.0', 'faiss-gpu>=1.7.1,<2.0.0'],
 'ngt': ['ngt>=1.8'],
 'nmslib': ['nmslib>=2.1.1,<3.0.0']}

setup_kwargs = {
    'name': 'kiez',
    'version': '0.4.0',
    'description': 'Hubness reduced nearest neighbor search for entity alignment with knowledge graph embeddings',
    'long_description': '<p align="center">\n<img src="https://github.com/dobraczka/kiez/raw/main/docs/kiezlogo.png" alt="kiez logo", width=200/>\n</p>\n\n<h2 align="center"> <a href="https://dbs.uni-leipzig.de/file/KIEZ_KEOD_2021_Obraczka_Rahm.pdf">kiez</a></h2>\n\n<p align="center">\n<a href="https://github.com/dobraczka/kiez/actions/workflows/main.yml"><img alt="Actions Status" src="https://github.com/dobraczka/kiez/actions/workflows/main.yml/badge.svg?branch=main"></a>\n<a href="https://github.com/dobraczka/kiez/actions/workflows/quality.yml"><img alt="Actions Status" src="https://github.com/dobraczka/kiez/actions/workflows/quality.yml/badge.svg?branch=main"></a>\n<a href=\'https://kiez.readthedocs.io/en/latest/?badge=latest\'><img src=\'https://readthedocs.org/projects/kiez/badge/?version=latest\' alt=\'Documentation Status\' /></a>\n<a href="https://codecov.io/gh/dobraczka/kiez"><img src="https://codecov.io/gh/dobraczka/kiez/branch/main/graph/badge.svg?token=AHBYFKJVLV"/></a>\n<a href="https://pypi.org/project/kiez"/><img alt="Stable python versions" src="https://img.shields.io/pypi/pyversions/kiez"></a>\n<a href="https://github.com/dobraczka/kiez/blob/main/LICENSE"><img alt="License BSD3 - Clause" src="https://img.shields.io/badge/license-BSD--3--Clause-blue"></a>\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n</p>\n\nA Python library for hubness reduced nearest neighbor search for the task of entity alignment with knowledge graph embeddings. The term kiez is a [german word](https://en.wikipedia.org/wiki/Kiez) that refers to a city neighborhood.\n\n## Hubness Reduction\nHubness is a phenomenon that arises in high-dimensional data and describes the fact that a couple of entities are nearest neighbors (NN) of many other entities, while a lot of entities are NN to no one.\nFor entity alignment with knowledge graph embeddings we rely on NN search. Hubness therefore is detrimental to our matching results.\nThis library is intended to make hubness reduction techniques available to data integration projects that rely on (knowledge graph) embeddings in their alignment process. Furthermore kiez incorporates several approximate nearest neighbor (ANN) libraries, to pair the speed advantage of approximate neighbor search with increased accuracy of hubness reduction.\n\n## Installation\nYou can install kiez via pip:\n``` bash\npip install kiez\n```\n\nTo make kiez faster it is recommended to install [faiss](https://github.com/facebookresearch/faiss) as well (if you do not already have it in your environment):\n\n``` bash\npip install kiez[faiss-cpu]\n```\n\nor if you have a gpu:\n``` bash\npip install kiez[faiss-gpu]\n```\nIf you need specific cuda versions for faiss see their [installation instructions](https://github.com/facebookresearch/faiss/blob/main/INSTALL.md) and install it seperately.\n\nYou can also get other specific libraries with e.g.:\n\n``` bash\n  pip install kiez[nmslib]\n```\n\nIf you want to install all of them use:\n\n``` bash\n  pip install kiez[all]\n```\n\n\n\n## Usage\nSimple nearest neighbor search for source entities in target space:\n``` python\nfrom kiez import Kiez\nimport numpy as np\n# create example data\nrng = np.random.RandomState(0)\nsource = rng.rand(100,50)\ntarget = rng.rand(100,50)\n# fit and get neighbors\nk_inst = Kiez()\nk_inst.fit(source, target)\nnn_dist, nn_ind = k_inst.kneighbors()\n```\nUsing (A)NN libraries and hubness reduction methods:\n``` python\nfrom kiez import Kiez\nimport numpy as np\n# create example data\nrng = np.random.RandomState(0)\nsource = rng.rand(100,50)\ntarget = rng.rand(100,50)\n# prepare algorithm and hubness reduction\nfrom kiez.neighbors import Faiss\nfaiss = Faiss(n_candidates=10)\nfrom kiez.hubness_reduction import CSLS\nhr = CSLS()\n# fit and get neighbors\nk_inst = Kiez(n_neighbors=5, algorithm=faiss, hubness=hr)\nk_inst.fit(source, target)\nnn_dist, nn_ind = k_inst.kneighbors()\n```\n\n## Documentation\nYou can find more documentation on [readthedocs](https://kiez.readthedocs.io)\n\n## Benchmark\nThe results and configurations of our experiments can be found in a seperate [benchmarking repository](https://github.com/dobraczka/kiez-benchmarking)\n\n## Citation\nIf you find this work useful you can use the following citation:\n```\n@inproceedings{Kiez,\n  author    = {Daniel Obraczka and\n               Erhard Rahm},\n  editor    = {David Aveiro and\n               Jan L. G. Dietz and\n               Joaquim Filipe},\n  title     = {An Evaluation of Hubness Reduction Methods for Entity Alignment with\n               Knowledge Graph Embeddings},\n  booktitle = {Proceedings of the 13th International Joint Conference on Knowledge\n               Discovery, Knowledge Engineering and Knowledge Management, {IC3K}\n               2021, Volume 2: KEOD, Online Streaming, October 25-27, 2021},\n  pages     = {28--39},\n  publisher = {{SCITEPRESS}},\n  year      = {2021},\n  url       = {https://dbs.uni-leipzig.de/file/KIEZ_KEOD_2021_Obraczka_Rahm.pdf},\n  doi       = {10.5220/0010646400003064},\n}\n```\n\n## Contributing\nPRs and enhancement ideas are always welcome. If you want to build kiez locally use:\n```bash\ngit clone git@github.com:dobraczka/kiez.git\ncd kiez\npoetry install\n```\nTo run the tests (given you are in the kiez folder):\n```bash\npoetry run pytest tests\n```\n\nOr install [nox](https://github.com/theacodes/nox) and run:\n```\nnox\n```\nwhich check all the linting as well.\n\n## License\n`kiez` is licensed under the terms of the BSD-3-Clause [license](LICENSE.txt).\nSeveral files were modified from [`scikit-hubness`](https://github.com/VarIr/scikit-hubness),\ndistributed under the same [license](external/SCIKIT_HUBNESS_LICENSE.txt).\nThe respective files contain the following tag instead of the full license text.\n\n        SPDX-License-Identifier: BSD-3-Clause\n\nThis enables machine processing of license information based on the SPDX\nLicense Identifiers that are here available: https://spdx.org/licenses/\n',
    'author': 'Daniel Obraczka',
    'author_email': 'obraczka@informatik.uni-leipzig.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dobraczka/kiez',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
