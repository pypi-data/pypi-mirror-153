# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tumorevo', 'tumorevo.tumorfig', 'tumorevo.tumorsim']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0',
 'networkx>=2.6.2,<3.0.0',
 'numpy>=1.21.2,<2.0.0',
 'packcircles>=0.14,<0.15',
 'pandas>=1.3.2,<2.0.0',
 'pygraphviz>=1.7,<2.0',
 'pymuller>=0.1.2,<0.2.0',
 'tqdm>=4.57.0,<5.0.0']

entry_points = \
{'console_scripts': ['tumorfig = tumorevo.tumorfig:main',
                     'tumorsim = tumorevo.tumorsim:main']}

setup_kwargs = {
    'name': 'tumorevo',
    'version': '0.0.1',
    'description': 'Simulate and illustrate tumor evolution under different spatial constraints.',
    'long_description': '# tumorevo\n\n[![PyPI](https://img.shields.io/pypi/v/tumorevo.svg?style=flat)](https://pypi.python.org/pypi/tumorevo)\n[![Tests](https://github.com/pedrofale/tumorevo/actions/workflows/main.yaml/badge.svg)](https://github.com/pedrofale/tumorevo/actions/workflows/main.yaml)\n\nSimulate tumor evolution under different spatial constraints. This package aims to be as awesome as [demon](https://github.com/robjohnnoble/demon_model).\n`tumorevo` simulates tumor growth and and produces a Muller plot, a cartoon of the 2D spatial organization of the tumor cells, and a clone tree.\n\n## Installation\n\n```bash\n$ pip install tumorevo\n```\n\n## Usage\n\n`tumorevo` contains two command line utilities: `tumorsim` and `tumorfig`.\n\n### Simulating tumor evolution\n`tumorsim` can be used to simulate the evolution of a tumor according to a specified spatial structure.\n```bash\n$ tumorsim --mode 1 --steps 2000 --genes 20 --carrying-capacity 5 --grid-size 20 --division-rate 0.2 --dispersal-rate 0.1\n100%|████████████████████| 1999/1999 [00:07<00:00, 251.69it/s]\n```\n\nThis will create a folder containing:\n* `parents.csv`: file indicating each clones\'s parent;\n* `trace_counts.csv`: file indicating the number of cells of each clone at each time step;\n* `genotypes.csv`: file containing the genotypes of each clone;\n* `grid.csv`: file containing the regular grid of genotypes if `mode` > 0.\n\nFull overview:\n```\n$ tumorsim --help\nUsage: tumorsim [OPTIONS]\n\n  Simulate tumor evolution under different spatial constraints.\n\nOptions:\n  -m, --mode INTEGER              Spatial structure.\n  -k, --carrying-capacity INTEGER\n                                  Deme carrying capacity.\n  -g, --genes INTEGER             Number of genes.\n  -s, --steps INTEGER             Number of steps in simulation.\n  --grid-size INTEGER             Grid size.\n  --division-rate FLOAT           Divison rate.\n  --mutation-rate FLOAT           Mutation rate.\n  --dispersal-rate FLOAT          Dispersal rate.\n  -r, --random_seed INTEGER       Random seed for the pseudo random number\n                                  generator.\n  --log INTEGER                   Logging level. 0 for no logging, 1 for info,\n                                  2 for debug.\n  -o, --output-path TEXT          Output directory\n  --help                          Show this message and exit.\n```\n\n### Plotting tumor evolution\n`tumorfig` can be used to create a Muller plot of the tumor\'s evolution, the 2D spatial organization of the tumor cells, and a clone tree.\n```bash\n$ tumorfig out/trace_counts.csv out/parents.csv --plot --grid-file out/grid.csv --normalize --remove\n```\n\nThis will open a figure like this:\n<div align="center">\n  <img src="https://github.com/pedrofale/tumorevo/raw/main/figures/example.png", width="700px">\n</div>\n\nFull overview:\n```\n$ tumorfig --help\nUsage: tumorfig [OPTIONS] GENOTYPE_COUNTS GENOTYPE_PARENTS\n\n  Plot the evolution of a tumor.\n\nOptions:\n  -c, --cells INTEGER           Number of cells in slice plot.\n  -r, --average-radius INTEGER  Average radius of circles in slice plot.\n  --grid-file TEXT              Path to grid file.\n  --colormap TEXT               Colormap for genotypes.\n  --dpi INTEGER                 DPI for figures.\n  --plot                        Plot all the figures.\n  --do-muller                   Make a Muller plot.\n  --do-slice                    Make a slice plot.\n  --do-tree                     Make a clone tree plot.\n  --normalize                   Normalize the abundances in the Muller plot.\n  --labels                      Annotate the clone tree plot.\n  --remove                      Remove empty clones in the clone tree plot.\n  -o, --output-path TEXT        Directory to write figures into.\n  --help                        Show this message and exit.\n```\n',
    'author': 'pedrofale',
    'author_email': 'pedro.miguel.ferreira.pf@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pedrofale/tumorevo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
