# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tpcp', 'tpcp._utils', 'tpcp.optimize', 'tpcp.validate']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.1.0,<2.0.0',
 'numpy>=1,<2',
 'pandas>=1,<2',
 'scikit-learn>=1,<2',
 'tqdm>=4.62.3,<5.0.0',
 'typing-extensions>=4.1.1']

extras_require = \
{'optuna': ['optuna>=2.10.0,<3.0.0'], 'torch': ['torch>=1.6.0']}

setup_kwargs = {
    'name': 'tpcp',
    'version': '0.6.3',
    'description': 'Pipeline and Dataset helpers for complex algorithm evaluation.',
    'long_description': '[![PyPI](https://img.shields.io/pypi/v/tpcp)](https://pypi.org/project/tpcp/)\n[![Documentation Status](https://readthedocs.org/projects/tpcp/badge/?version=latest)](https://tpcp.readthedocs.io/en/latest/?badge=latest)\n[![codecov](https://codecov.io/gh/mad-lab-fau/tpcp/branch/main/graph/badge.svg?token=ZNVT5LNYHO)](https://codecov.io/gh/mad-lab-fau/tpcp)\n[![Test and Lint](https://github.com/mad-lab-fau/tpcp/actions/workflows/test-and-lint.yml/badge.svg?branch=main)](https://github.com/mad-lab-fau/tpcp/actions/workflows/test-and-lint.yml)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/tpcp)\n\n# tpcp - Tiny Pipelines for Complex Problems\n\nA generic way to build object-oriented datasets and algorithm pipelines and tools to evaluate them.\n\nEasily install `tpcp` via pip:\n```bash\npip install tpcp\n```\n\nOr add it to your project with [poetry](https://python-poetry.org/):\n```bash\npoetry add tpcp\n```\n\n## Why?\n\nEvaluating Algorithms - in particular when they contain machine learning - is hard.\nBesides understanding required concepts (cross validation, bias, overfitting, ...), you need to implement the required \nsteps and make them work together with your algorithms and data.\nIf you are doing something "regular" like training an SVM on tabular data, amazing libraries like [sklearn](https://scikit-learn.org), \n[tslearn](https://github.com/tslearn-team/tslearn), [pytorch](https://pytorch.org), and many others, have your back.\nBy using their built-in tools (e.g. `sklearn.evaluation.GridSearchCV`) you prevent implementation errors, and you are\nprovided with a sensible structure to organize your code that is well understood in the community.\n\nHowever, often the problems we are trying to solve are not regular.\nThey are **complex**.\nAs an example, here is the summary of the method from one of our [recent papers](https://jneuroengrehab.biomedcentral.com/articles/10.1186/s12984-021-00883-7):\n- We have continuous multi-dimensional sensor recordings from multiple participants from a hospital visit and multiple days at home\n- For each participant we have global metadata (age, diagnosis) and daily annotations\n- We want to train a Hidden-Markov-Model that can find events in the data streams\n- We need to tune hyper-parameters of the algorithm using a participant-wise cross validation\n- We want to evaluate the final performance of the algorithm for the settings trained on the hospital data -> tested on home data and trained on home data -> tested on home data\n- Using the same structure we want to evaluate a state-of-the-art algorithm to compare the results\n\nNone of the standard frameworks can easily abstract this problem, because here we have none-tabular data, multiple data \nsources per participant, a non-traditional ML algorithm, and a complex train-test split logic.\n\nWith `tpcp` we want to provide a flexible framework to approach such complex problems with structure and confidence.\n\n## How?\n\nTo make `tpcp` easy to use, we try to focus on a couple of key ideas:\n\n- Datasets are Python classes (think of [`pytorch.datasets`](https://pytorch.org/tutorials/beginner/basics/data_tutorial.html), but more flexible) that can be split, iterated over, and queried.\n- Algorithms and Pipelines are Python classes with a simple `run` and `optimize` interface, that can be implemented to fit any problem.\n- Everything is a parameter and everything is optimization: In regular ML we differentiate *training* and *hyper-parameter optimization*.\n  In `tpcp` we consider everything that modifies parameters or weights as an *optimization*.\n  This allows to use the same concepts and code interfaces from simple algorithms that just require a grid search to optimize a parameter to neuronal network pipelines with hyperparameter tuning.\n- Provide what is difficult, allow to change everything else:\n  `tpcp` implements complicated constructs like cross validation and grid search and, whenever possible, tries to catch obvious errors in your approach.\n  However, for the actual algorithm and dataset you are free to do whatever is required to solve your current research question.\n\n## Projects that use tpcp\n\n#### Datasets\n\n- [sensor_position_dataset_helper](https://github.com/mad-lab-fau/sensor_position_dataset_helper/blob/master/sensor_position_dataset_helper/tpcp_dataset.py)\n- [cold-face-test-analysis](https://github.com/mad-lab-fau/cft-analysis/tree/main/cft_analysis/datasets)\n\n## Dev Setup\n\nWe are using [poetry](https://python-poetry.org/) to manage dependencies and \n[poethepoet](https://github.com/nat-n/poethepoet) to run and manage dev tasks.\n\nTo set up the dev environment *including* the required dependencies for using `tpcp` together with `optuna` \nrun the following commands: \n```bash\ngit clone https://github.com/mad-lab-fau/tpcp\ncd tpcp\npoetry install -E optuna -E torch # This might take a while\n```\n\n\nAfterwards you can start to develop and change things.\nIf you want to run tests, format your code, build the docs, ..., you can run one of the following `poethepoet` commands\n\n```\nCONFIGURED TASKS\n  format         \n  lint           Lint all files with Prospector.\n  check          Check all potential format and linting issues.\n  test           Run Pytest with coverage.\n  docs           Build the html docs using Sphinx.\n  bump_version   \n```\n\nby calling\n\n```bash\npoetry run poe <command name>\n````\n\nIf you installed `poethepoet` globally, you can skip the `poetry run` part at the beginning.\n\n## Contribution\n\nThe entire development is managed via [GitHub](https://github.com/mad-lab-fau/tpcp).\nIf you run into any issues, want to discuss certain decisions, want to contribute features or feature requests, just \nreach out to us by [opening a new issue](https://github.com/mad-lab-fau/tpcp/issues/new/choose).\n',
    'author': 'Arne Küderle',
    'author_email': 'arne.kuederle@fau.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mad-lab-fau/tpcp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
