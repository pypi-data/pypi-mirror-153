# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scvi',
 'scvi.data',
 'scvi.data._built_in_data',
 'scvi.data.fields',
 'scvi.dataloaders',
 'scvi.distributions',
 'scvi.external',
 'scvi.external.cellassign',
 'scvi.external.gimvi',
 'scvi.external.solo',
 'scvi.external.stereoscope',
 'scvi.model',
 'scvi.model.base',
 'scvi.model.utils',
 'scvi.module',
 'scvi.module.base',
 'scvi.nn',
 'scvi.train',
 'scvi.utils']

package_data = \
{'': ['*']}

install_requires = \
['anndata>=0.7.5',
 'docrep>=0.3.2',
 'flax',
 'h5py>=2.9.0',
 'ipywidgets',
 'jax>=0.3',
 'numpy>=1.17.0',
 'numpyro',
 'openpyxl>=3.0',
 'optax',
 'pandas>=1.0',
 'protobuf<=3.20.1',
 'pyro-ppl>=1.6.0',
 'pytorch-lightning>=1.5,<1.6',
 'rich>=9.1.0',
 'scikit-learn>=0.21.2',
 'torch>=1.8.0',
 'torchmetrics>=0.6.0',
 'tqdm>=4.56.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>1.0'],
 'dev': ['black>=22.3',
         'codecov>=2.0.8',
         'flake8>=3.7.7',
         'isort>=5.7',
         'jupyter>=1.0',
         'loompy>=3.0.6',
         'nbconvert>=5.4.0',
         'nbformat>=4.4.0',
         'pre-commit>=2.7.1',
         'pytest>=4.4',
         'scanpy>=1.6'],
 'docs': ['furo>=2022.2.14.1',
          'myst-parser',
          'nbsphinx',
          'nbsphinx-link',
          'scanpydoc>=0.5',
          'sphinx>=4.1',
          'sphinx-autodoc-typehints',
          'sphinx-design',
          'sphinx-gallery>0.6',
          'sphinx_copybutton<=0.3.1',
          'sphinx_remove_toctrees',
          'sphinxext-opengraph'],
 'docs:python_version < "3.8"': ['typing_extensions'],
 'docs:python_version >= "3.7"': ['ipython>=7.20'],
 'pymde': ['pymde'],
 'tutorials': ['leidenalg',
               'loompy>=3.0.6',
               'pymde',
               'pynndescent',
               'python-igraph',
               'scanpy>=1.6',
               'scikit-misc>=0.1.3']}

setup_kwargs = {
    'name': 'scvi-tools',
    'version': '0.16.3',
    'description': 'Deep probabilistic analysis of single-cell omics data.',
    'long_description': '<img src="https://github.com/scverse/scvi-tools/blob/master/docs/_static/scvi-tools-horizontal.svg?raw=true" width="400" alt="scvi-tools">\n\n[![Stars](https://img.shields.io/github/stars/scverse/scvi-tools?logo=GitHub&color=yellow)](https://github.com/YosefLab/scvi-tools/stargazers)\n[![PyPI](https://img.shields.io/pypi/v/scvi-tools.svg)](https://pypi.org/project/scvi-tools)\n[![Documentation Status](https://readthedocs.org/projects/scvi/badge/?version=latest)](https://scvi.readthedocs.io/en/stable/?badge=stable)\n![Build\nStatus](https://github.com/scverse/scvi-tools/workflows/scvi-tools/badge.svg)\n[![Coverage](https://codecov.io/gh/scverse/scvi-tools/branch/master/graph/badge.svg)](https://codecov.io/gh/YosefLab/scvi-tools)\n[![Code\nStyle](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)\n[![Downloads](https://pepy.tech/badge/scvi-tools)](https://pepy.tech/project/scvi-tools)\n[![Project chat](https://img.shields.io/badge/zulip-join_chat-brightgreen.svg)](https://scverse.zulipchat.com/)\n\n[scvi-tools](https://scvi-tools.org/) (single-cell variational inference\ntools) is a package for probabilistic modeling and analysis of single-cell omics\ndata, built on top of [PyTorch](https://pytorch.org) and\n[AnnData](https://anndata.readthedocs.io/en/latest/).\n\n# Analysis of single-cell omics data\n\nscvi-tools is composed of models that can perform one or more tasks in single-cell omics data analysis. scvi-tools currently hosts implementations of:\n\n-   [scVI](https://rdcu.be/bdHYQ) for analysis of single-cell RNA-seq\n    data, as well as its improved differential expression\n    [framework](https://www.biorxiv.org/content/biorxiv/early/2019/10/04/794289.full.pdf).\n-   [scANVI](https://www.biorxiv.org/content/biorxiv/early/2019/01/29/532895.full.pdf)\n    for cell annotation of scRNA-seq data using semi-labeled examples.\n-   [totalVI](https://www.biorxiv.org/content/10.1101/2020.05.08.083337v1.full.pdf)\n    for analysis of CITE-seq data.\n-   [gimVI](https://arxiv.org/pdf/1905.02269.pdf) for imputation of\n    missing genes in spatial transcriptomics from scRNA-seq data.\n-   [AutoZI](https://www.biorxiv.org/content/biorxiv/early/2019/10/10/794875.full.pdf)\n    for assessing gene-specific levels of zero-inflation in scRNA-seq\n    data.\n-   [LDVAE](https://www.biorxiv.org/content/10.1101/737601v1.full.pdf)\n    for an interpretable linear factor model version of scVI.\n-   [Stereoscope](https://www.nature.com/articles/s42003-020-01247-y)\n    for deconvolution of spatial transcriptomics data.\n-   [DestVI](https://www.biorxiv.org/content/10.1101/2021.05.10.443517v1) for multi-resolution deconvolution\n    of spatial transcriptomics data.\n-   [peakVI](https://www.biorxiv.org/content/10.1101/2021.04.29.442020v1) for analysis of scATAC-seq data.\n-   [scArches](https://www.biorxiv.org/content/10.1101/2020.07.16.205997v1)\n    for transfer learning from one single-cell atlas to a query dataset\n    (currently supports scVI, scANVI and TotalVI).\n-   [CellAssign](https://www.nature.com/articles/s41592-019-0529-1) for\n    reference-based annotation of scRNA-seq data.\n-   [Solo](https://www.sciencedirect.com/science/article/pii/S2405471220301952)\n    for doublet detection in scRNA-seq data.\n\nAll these implementations have a high-level API that interacts with\n[scanpy](http://scanpy.readthedocs.io/), standard save/load functions,\nand support GPU acceleration.\n\n# Rapid development of novel probabilistic models\n\nscvi-tools contains the building blocks to develop and deploy novel probablistic\nmodels. These building blocks are powered by popular probabilistic and\nmachine learning frameworks such as [PyTorch\nLightning](https://www.pytorchlightning.ai/) and\n[Pyro](https://pyro.ai/). For an overview of how the scvi-tools package\nis structured, you may refer to [this](https://docs.scvi-tools.org/en/stable/user_guide/background/codebase_overview.html) page.\n\nWe recommend checking out the [skeleton\nrepository](https://github.com/YosefLab/scvi-tools-skeleton) as a\nstarting point for developing and deploying new models with scvi-tools.\n\n# Basic installation\n\nFor conda,\n```\nconda install scvi-tools -c conda-forge\n```\nand for pip,\n```\npip install scvi-tools\n```\nPlease be sure to install a version of [PyTorch](https://pytorch.org/) that is compatible with your GPU (if applicable).\n\n# Resources\n\n-   Tutorials, API reference, and installation guides are available in\n    the [documentation](https://docs.scvi-tools.org/).\n-   For discussion of usage, check out our\n    [forum](https://discourse.scvi-tools.org).\n-   Please use the [issues](https://github.com/scverse/scvi-tools/issues) to submit bug reports.\n-   If you\\\'d like to contribute, check out our [contributing\n    guide](https://docs.scvi-tools.org/en/stable/contributing/index.html).\n-   If you find a model useful for your research, please consider citing\n    the corresponding publication (linked above).\n\n# Reference\n\nIf you used scvi-tools in your research, please consider citing\n\n```\n@article{Gayoso2022,\n         author={Gayoso, Adam and Lopez, Romain and Xing, Galen and Boyeau, Pierre and Valiollah Pour Amiri, Valeh and Hong, Justin and Wu, Katherine and Jayasuriya, Michael and   Mehlman, Edouard and Langevin, Maxime and Liu, Yining and Samaran, Jules and Misrachi, Gabriel and Nazaret, Achille and Clivio, Oscar and Xu, Chenling and Ashuach, Tal and Gabitto, Mariano and Lotfollahi, Mohammad and Svensson, Valentine and da Veiga Beltrame, Eduardo and Kleshchevnikov, Vitalii and Talavera-L{\\\'o}pez, Carlos and Pachter, Lior and Theis, Fabian J. and Streets, Aaron and Jordan, Michael I. and Regier, Jeffrey and Yosef, Nir},\n         title={A Python library for probabilistic analysis of single-cell omics data},\n         journal={Nature Biotechnology},\n         year={2022},\n         month={Feb},\n         day={07},\n         issn={1546-1696},\n         doi={10.1038/s41587-021-01206-w},\n         url={https://doi.org/10.1038/s41587-021-01206-w}\n}\n```\nalong with the publicaton describing the model used. \n\n',
    'author': 'The scvi-tools development team',
    'author_email': 'adamgayoso@berkeley.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/scverse/scvi-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
