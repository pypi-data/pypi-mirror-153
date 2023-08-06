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
 'cupy>=10.4.0,<11.0.0',
 'fastparquet>=0.8.1,<0.9.0',
 'geopandas>=0.10.2,<0.11.0',
 'joblib>=1.1.0,<2.0.0',
 'loguru>=0.6.0,<0.7.0',
 'matplotlib>=3.5.1,<4.0.0',
 'networkx>=2.6.3,<3.0.0',
 'optuna>=2.10.0,<3.0.0',
 'ruamel.yaml>=0.17.20,<0.18.0',
 'scikit-optimize>=0.9.0,<0.10.0',
 'scipy>=1.7.3,<2.0.0',
 'tqdm>=4.62.3,<5.0.0',
 'typer>=0.4.0,<0.5.0',
 'us>=2.0.2,<3.0.0']

extras_require = \
{':python_full_version >= "3.7.1" and python_version < "3.8"': ['pandas>=1.3.0,<1.4.0'],
 ':python_version < "3.8"': ['numpy==1.21.5'],
 ':python_version >= "3.8"': ['numpy>=1.22.1,<2.0.0', 'pandas>=1.4.0,<2.0.0']}

entry_points = \
{'console_scripts': ['bucky = bucky.cli.main:main']}

setup_kwargs = {
    'name': 'bucky-covid',
    'version': '1.0.0a0',
    'description': 'The Bucky model is a spatial SEIR model for simulating COVID-19 at the county level.',
    'long_description': "# Bucky Model \n[![Documentation Status](https://readthedocs.org/projects/docs/badge/?version=latest)](https://bucky.readthedocs.io/en/latest/)\n![black-flake8-isort-hooks](https://github.com/mattkinsey/bucky/workflows/black-flake8-isort-hooks/badge.svg)\n[![CodeFactor](https://www.codefactor.io/repository/github/mattkinsey/bucky/badge/master)](https://www.codefactor.io/repository/github/mattkinsey/bucky/overview/master)\n![Interrogate](docs/_static/interrogate_badge.svg)\n\n**[Documentation](https://bucky.readthedocs.io/en/latest/)**\n\n**[Developer Guide](https://github.com/mattkinsey/bucky/blob/poetry/dev_readme.md)**\n\nThe Bucky model is a spatial SEIR model for simulating COVID-19 at the county level. \n\n## Getting Started\n\n### Requirements\nThe Bucky model currently supports Linux and OSX and includes GPU support for accelerated modeling and processing.\n\n* ``git`` must be installed and in your PATH.\n* GPU support requires a cupy-compatible CUDA installation. See the [CuPy docs](https://docs.cupy.dev/en/stable/install.html#requirements) for details.\n\n### Installation\n\n| !! Until the PyPi release you'll need to install via poetry !!                                            |\n|:----------------------------------------------------------------------------------------------------------|\n| See the [Developer Guide](https://github.com/mattkinsey/bucky/blob/poetry/dev_readme.md) for instructions.|\n\nStandard installation:\n```bash\npip install bucky-covid\n```\nGPU installation:\n```bash\npip install bucky-covid[gpu]\n```\n\n### Configuration (TODO this is WIP)\nTo use a customized configuration you first need to make a local copy of the bucky configuration. In your working directory:\n```bash\nbucky cfg install-local\n```\n\n### Download Input Data\nTo download the required input data to the ``data_dir`` specified in the configuration files:\n```bash\nbucky data sync\n```\n\n### Running the Model\n\n```bash\nbucky run model [TODO enum params]\nbucky run postprocess\n```\n\n\n---------------------\n\n**!!! EVERYTHING BELOW HERE IS OUTDATED FOR THE NEW CLI !!!**\n\nIn order to illustrate how to run the model, this section contains the commands needed to run a small simulation. First, create the intermediate graph format used by the model. This graph contains county-level data on the nodes and mobility information on the edges. The command below creates a US graph for a simulation that will start on October 1, 2020. \n\n```console\n./bmodel make_input_graph -d 2020-10-01\n```\n\nAfter creating the graph, run the model with 100 iterations and 20 days:\n\n```console\n./bmodel model -n 100 -d 20\n```\n\nThis will create a folder in the `raw_output` directory with the unique run ID. The script `postprocess` processes and aggregates the Monte Carlo runs. This script by default postprocesses the most recent data in the `raw_output` directory and aggregates at the national, state, and county level.\n\n```console\n./bmodel postprocess\n```\n\n### Visualizing Results\nTo create plots:\n\n```console\n./bmodel viz.plot\n```\n\nLike postprocessing, this script by default creates plots for the most recently processed data. Plots will be located in `output/<run_id>/plots`. These plots can be customized to show different columns and historical data. See the documentation for more.\n\n### Lookup Tables\nDuring postprocessing, the graph file is used to define geographic relationships between administrative levels (e.g. counties, states). In some cases, a user may want to define custom geographic groupings for visualization and analysis. For example, the National Capital Region includes counties from Maryland and Virginia along with Washington, DC. An example lookup table for this region (also known as the DMV) is included in the repo, *DMV.lookup*. \n\nTo aggregate data with this lookup table, use the flag `--lookup` followed by the path to the lookup file:\n\n```console\n    ./bmodel postprocess --lookup DMV.lookup\n```\nThis will create a new directory with the prefix *DMV_* in the default output directory (output/DMV_<run_id>/). To plot:\n\n```console\n  ./bmodel model viz.plot --lookup DMV.lookup\n```\n",
    'author': 'Matt Kinsey',
    'author_email': 'matt@mkinsey.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://buckymodel.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
