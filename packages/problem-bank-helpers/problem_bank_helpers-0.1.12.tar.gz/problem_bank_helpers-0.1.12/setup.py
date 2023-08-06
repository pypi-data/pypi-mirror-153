# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['problem_bank_helpers']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.3,<2.0.0', 'sigfig>=1.1.9,<2.0.0']

setup_kwargs = {
    'name': 'problem-bank-helpers',
    'version': '0.1.12',
    'description': 'Helpful utilities for the open problem bank.',
    'long_description': '# Problem Bank Helpers \n\n[![Python](https://img.shields.io/badge/python-3.9-blue)]()\n[![codecov](https://codecov.io/gh/open-resources/problem_bank_helpers/branch/main/graph/badge.svg)](https://codecov.io/gh/open-resources/problem_bank_helpers)\n[![Documentation Status](https://readthedocs.org/projects/problem_bank_helpers/badge/?version=latest)](https://problem_bank_helpers.readthedocs.io/en/latest/?badge=latest)\n\n\n## Installation\n\n```bash\n$ pip install -i https://test.pypi.org/simple/ problem_bank_helpers\n```\n\n## Features\n\n- TODO\n\n## Dependencies\n\n- TODO\n\n## Usage\n\n- TODO\n\n## Documentation\n\nThe official documentation is hosted on Read the Docs: https://problem_bank_helpers.readthedocs.io/en/latest/\n\n## Contributors\n\nWe welcome and recognize all contributions. You can see a list of current contributors in the [contributors tab](https://github.com/open-resources/problem_bank_helpers/graphs/contributors).\n\n### Credits\n\nThis package was created with Cookiecutter and the UBC-MDS/cookiecutter-ubc-mds project template, modified from the [pyOpenSci/cookiecutter-pyopensci](https://github.com/pyOpenSci/cookiecutter-pyopensci) project template and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage).\n',
    'author': 'Firas Moosvi and Jake Bobowski',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/open-resources/problem_bank_helpers',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
