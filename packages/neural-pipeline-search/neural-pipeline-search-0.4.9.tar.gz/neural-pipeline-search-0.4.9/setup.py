# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neps',
 'neps.optimizers',
 'neps.optimizers.bayesian_optimization',
 'neps.optimizers.bayesian_optimization.acquisition_functions',
 'neps.optimizers.bayesian_optimization.acquisition_samplers',
 'neps.optimizers.bayesian_optimization.kernels',
 'neps.optimizers.bayesian_optimization.kernels.grakel_replace',
 'neps.optimizers.bayesian_optimization.models',
 'neps.optimizers.grid_search',
 'neps.optimizers.random_search',
 'neps.optimizers.regularized_evolution',
 'neps.search_spaces',
 'neps.search_spaces.graph_dense',
 'neps.search_spaces.graph_grammar',
 'neps.search_spaces.graph_grammar.cfg_variants',
 'neps.search_spaces.graph_grammar.graph_utils',
 'neps.search_spaces.numerical',
 'neps.status',
 'neps.utils',
 'neps_examples',
 'neps_examples.cost_aware',
 'neps_examples.fault_tolerance',
 'neps_examples.hierarchical_architecture',
 'neps_examples.hierarchical_architecture_hierarchical_GP',
 'neps_examples.hierarchical_kernels',
 'neps_examples.hyperparameters',
 'neps_examples.hyperparameters_architecture',
 'neps_examples.multi_fidelity',
 'neps_examples.user_priors',
 'neps_examples.user_priors_also_architecture']

package_data = \
{'': ['*']}

install_requires = \
['ConfigSpace>=0.4.19,<0.5.0',
 'grakel>=0.1.8,<0.2.0',
 'matplotlib>=3.4,<4.0',
 'metahyper>=0.5.3,<0.6.0',
 'networkx>=2.6.3,<3.0.0',
 'nltk>=3.6.4,<4.0.0',
 'numpy>=1.21.1,<2.0.0',
 'pandas>=1.3.1,<2.0.0',
 'path>=16.2.0,<17.0.0',
 'scipy>=1.7,<2.0',
 'termcolor>=1.1.0,<2.0.0',
 'torch>=1.7.0',
 'types-termcolor>=1.1.2,<2.0.0',
 'typing-extensions>=4.0.1,<5.0.0']

setup_kwargs = {
    'name': 'neural-pipeline-search',
    'version': '0.4.9',
    'description': 'Neural Pipeline Search helps deep learning experts find the best neural pipeline.',
    'long_description': '# Neural Pipeline Search\n\nNeural Pipeline Search helps deep learning experts find the best neural pipeline.\n\nFeatures:\n\n- Hyperparameter optimization (HPO)\n- Neural architecture search (NAS): cell-based and hierarchical\n- Joint NAS and HPO\n- Expert priors to guide the search\n- Asynchronous parallelization and distribution\n- Fault tolerance for crashes and job time limits\n\nSoon-to-come Features:\n\n- Multi-fidelity\n- Cost-aware\n- Across code version transfer\n- Python 3.8+ support\n- Multi-objective\n\n![Python versions](https://img.shields.io/badge/python-3.7-informational)\n[![License](https://img.shields.io/badge/license-Apache%202.0-informational)](LICENSE)\n[![Tests](https://github.com/automl/neps/actions/workflows/tests.yaml/badge.svg)](https://github.com/automl/neps/actions)\n\n## Installation\n\nUsing pip\n\n```bash\npip install neural-pipeline-search\n```\n\n### Optional: Specific torch versions\n\nIf you run into any issues regarding versions of the torch ecosystem (like needing cuda enabled versions), you might want to use our utility\n\n```bash\npython -m neps.utils.install_torch\n```\n\nThis script asks for the torch version you want and installs all the torch libraries needed for the neps package with\nthat version. For the installation `pip` of the active python environment is used.\n\n## Usage\n\nUsing `neps` always follows the same pattern:\n\n1. Define a `run_pipeline` function that evaluates architectures/hyperparameters for your problem\n1. Define a search space `pipeline_space` of architectures/hyperparameters\n1. Call `neps.run` to optimize `run_pipeline` over `pipeline_space`\n\nIn code the usage pattern can look like this:\n\n```python\nimport neps\nimport logging\n\n# 1. Define a function that accepts hyperparameters and computes the validation error\ndef run_pipeline(hyperparameter_a: float, hyperparameter_b: int):\n    validation_error = -hyperparameter_a * hyperparameter_b\n    return validation_error\n\n\n# 2. Define a search space of hyperparameters; use the same names as in run_pipeline\npipeline_space = dict(\n    hyperparameter_a=neps.FloatParameter(lower=0, upper=1),\n    hyperparameter_b=neps.IntegerParameter(lower=1, upper=100),\n)\n\n# 3. Call neps.run to optimize run_pipeline over pipeline_space\nlogging.basicConfig(level=logging.INFO)\nneps.run(\n    run_pipeline=run_pipeline,\n    pipeline_space=pipeline_space,\n    working_directory="usage_example",\n    max_evaluations_total=5,\n)\n```\n\n### More examples\n\nFor more usage examples for features of neps have a look at [neps_examples](neps_examples).\n\n### Status information\n\nTo show status information about a neural pipeline search use\n\n```bash\npython -m neps.status WORKING_DIRECTORY\n```\n\nIf you need more status information than is printed per default (e.g., the best config over time), please have a look at\n\n```bash\npython -m neps.status --help\n```\n\nTo show the status repeatedly, on unix systems you can use\n\n```bash\nwatch --interval 30 python -m neps.status WORKING_DIRECTORY\n```\n\n### Parallelization\n\nIn order to run a neural pipeline search with multiple processes or multiple machines, simply call `neps.run` multiple times.\nAll calls to `neps.run` need to use the same `working_directory` on the same filesystem, otherwise there is no synchronization between the `neps.run`\'s.\n\n## Contributing\n\nPlease see our guidelines and guides for contributors at [CONTRIBUTING.md](CONTRIBUTING.md).\n',
    'author': 'Danny Stoll',
    'author_email': 'stolld@cs.uni-freiburg.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/automl/neps',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.8',
}


setup(**setup_kwargs)
