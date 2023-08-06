# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['problem_bank_scripts']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'docopt>=0.6.2,<0.7.0',
 'markdown-it-py>=1.1.0,<2.0.0',
 'mdformat>=0.7.6,<0.8.0',
 'numpy>=1.20.3,<2.0.0',
 'pandas>=1.2.4,<2.0.0',
 'problem-bank-helpers>=0.1.3,<0.2.0',
 'sympy>=1.8,<2.0']

setup_kwargs = {
    'name': 'problem-bank-scripts',
    'version': '0.3.5',
    'description': 'A packagee with useful functions to convert between different problem bank formats.',
    'long_description': '# Problem Bank Scripts \n\n[![Python](https://img.shields.io/badge/python-3.9-blue)]()\n[![codecov](https://codecov.io/gh/open-resources/problem_bank_scripts/branch/main/graph/badge.svg)](https://codecov.io/gh/open-resources/problem_bank_scripts)\n[![Documentation Status](https://readthedocs.org/projects/problem_bank_scripts/badge/?version=latest)](https://problem_bank_scripts.readthedocs.io/en/latest/?badge=latest)\n\n\n## Installation\n\n```bash\n$ pip install -i https://test.pypi.org/simple/ problem_bank_scripts\n```\n\n## Features\n\n- TODO\n\n## Dependencies\n\n- TODO\n\n## Usage\n\n- TODO\n\n## Documentation\n\nThe official documentation is hosted on Read the Docs: https://problem_bank_scripts.readthedocs.io/en/latest/\n\n## Contributors\n\nWe welcome and recognize all contributions. You can see a list of current contributors in the [contributors tab](https://github.com/open-resources/problem_bank_scripts/graphs/contributors).\n\n### Credits\n\nThis package was created with Cookiecutter and the UBC-MDS/cookiecutter-ubc-mds project template, modified from the [pyOpenSci/cookiecutter-pyopensci](https://github.com/pyOpenSci/cookiecutter-pyopensci) project template and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage).\n',
    'author': 'Open Problem Bank Team',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/open-resources/problem_bank_scripts',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
