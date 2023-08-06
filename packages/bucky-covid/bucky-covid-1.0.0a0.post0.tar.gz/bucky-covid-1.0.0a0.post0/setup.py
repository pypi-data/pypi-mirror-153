# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bucky',
 'bucky.cli',
 'bucky.data',
 'bucky.datasource_transforms',
 'bucky.model',
 'bucky.util',
 'bucky.viz']

package_data = \
{'': ['*'],
 'bucky': ['base_config/*',
           'included_data/*',
           'included_data/lookup_tables/*',
           'included_data/population/*',
           'included_data/vaccine_hesitancy/*']}

install_requires = \
['PyQt5>=5.15.6,<6.0.0',
 'better-exceptions>=0.3.3,<0.4.0',
 'cupy>=10.5.0,<11.0.0',
 'fastparquet>=0.8.1,<0.9.0',
 'geopandas>=0.10.2,<0.11.0',
 'joblib>=1.1.0,<2.0.0',
 'loguru>=0.6.0,<0.7.0',
 'matplotlib>=3.5.2,<4.0.0',
 'numpy>=1.22.4,<2.0.0',
 'optuna>=2.10.0,<3.0.0',
 'pandas>=1.4.2,<2.0.0',
 'ruamel.yaml>=0.17.21,<0.18.0',
 'scikit-optimize>=0.9.0,<0.10.0',
 'scipy>=1.8.1,<2.0.0',
 'tqdm>=4.64.0,<5.0.0',
 'typer>=0.4.1,<0.5.0',
 'us>=2.0.2,<3.0.0']

entry_points = \
{'console_scripts': ['bucky = bucky.cli.main:main']}

setup_kwargs = {
    'name': 'bucky-covid',
    'version': '1.0.0a0.post0',
    'description': 'The Bucky model is a spatial SEIR model for simulating COVID-19 at the county level.',
    'long_description': "# Bucky Model \n[![Documentation Status](https://readthedocs.org/projects/docs/badge/?version=latest)](https://bucky.readthedocs.io/en/latest/)\n![black-flake8-isort-hooks](https://github.com/mattkinsey/bucky/workflows/black-flake8-isort-hooks/badge.svg)\n[![CodeFactor](https://www.codefactor.io/repository/github/mattkinsey/bucky/badge/master)](https://www.codefactor.io/repository/github/mattkinsey/bucky/overview/master)\n![Interrogate](docs/_static/interrogate_badge.svg)\n\n**[Documentation](https://bucky.readthedocs.io/en/latest/)**\n\n**[Developer Guide](https://github.com/mattkinsey/bucky/blob/poetry/dev_readme.md)**\n\nThe Bucky model is a spatial SEIR model for simulating COVID-19 at the county level. \n\n## Getting Started\n\n### Requirements\nThe Bucky model currently supports Linux and OSX and includes GPU support for accelerated modeling and processing.\n\n* ``git`` must be installed and in your PATH.\n* GPU support requires a cupy-compatible CUDA installation. See the [CuPy docs](https://docs.cupy.dev/en/stable/install.html#requirements) for details.\n\n### Installation\n\nStandard installation:\n```bash\npip install bucky-covid\n```\n\n### Choose a working directory\nBucky will produce multiple folders for historical data and outputs. It's recommended to put these in their own directory, for example ``~/bucky``\n```bash\nBUCKY_DIR=~/bucky\nmkdir $BUCKY_DIR\ncd $BUCKY_DIR\n```\n\n### Configuration\nThe default configuration for bucky is located [here](https://github.com/mattkinsey/bucky/tree/master/bucky/base_config). Currently, you can locally modify these options by creating a ``bucky.yml`` in ``BUCKY_DIR`` that will override any of the default options specified in it.\n\nTODO this is WIP and does not work yet:\n\n~~To use a customized configuration you first need to make a local copy of the bucky configuration. In your working directory:~~\n```bash\nbucky cfg install-local\n```\n\n### Download Input Data\nTo download the required input data to the ``data_dir`` specified in the configuration files (default is ```$(pwd)/data```:\n```bash\nbucky data sync\n```\n\n### Running the Model\nTo run the model with default settings and produce standard outputs.\n```bash\nbucky run\n```\n\nEquivalently, one can the following command (to provide cli configuration to each part of the process)\n```bash\nbucky run model\nbucky run postprocess\nbucky viz plot\n```\n\n### CLI options\nEach ```bucky``` command has options that can be detailed with the ``--help`` flag. e.g.\n\n    $ bucky run model --help\n    \n    Usage: bucky run model [OPTIONS]\n    \n      `bucky run model`, run the model itself, dumping raw monte\n      carlo output to raw_output_dir.\n    \n    Options:\n      -d INTEGER         Number of days to project forward\n                         [default: 30]\n      -s INTEGER         Global PRNG seed  [default: 42]\n      -n INTEGER         Number of Monte Carlo iterations  [default:\n                         100]\n      --runid TEXT       UUID name of current run  [default:\n                         2022-06-04__08_00_03]\n      --start-date TEXT  Start date for the simulation. (YYYY-MM-DD)\n      --help             Show this message and exit.\n\nFurther CLI documentation is available in the [documentation](https://docs.buckymodel.com/en/latest/cli.html).\n",
    'author': 'Matt Kinsey',
    'author_email': 'matt@mkinsey.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://buckymodel.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
