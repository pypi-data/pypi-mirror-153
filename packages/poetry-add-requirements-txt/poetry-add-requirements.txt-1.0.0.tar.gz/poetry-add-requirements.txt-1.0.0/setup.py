# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_add_requirements_txt']

package_data = \
{'': ['*']}

install_requires = \
['charset-normalizer>=2.0.12,<3.0.0']

entry_points = \
{'console_scripts': ['poeareq = poetry_add_requirements_txt.cli:main',
                     'poetry-add-requirements.txt = '
                     'poetry_add_requirements_txt.cli:main']}

setup_kwargs = {
    'name': 'poetry-add-requirements.txt',
    'version': '1.0.0',
    'description': 'Add dependencies specified in requirements.txt to your Poetry project',
    'long_description': '# poetry-add-requirements.txt\n\nAdd dependencies specified in requirements.txt to your Poetry project\n\n- [poetry-add-requirements.txt](#poetry-add-requirementstxt)\n  - [Installation](#installation)\n    - [pipx](#pipx)\n    - [pip](#pip)\n  - [Usage](#usage)\n  - [Develop](#develop)\n\n## Installation\n\n### pipx\n\nThis is the recommended installation method.\n\n```\n$ pipx install poetry-add-requirements.txt\n```\n\n### [pip](https://pypi.org/project/poetry-add-requirements.txt/)\n\n```\n$ pip install poetry-add-requirements.txt\n```\n\n## Usage\n\nRun `poetry-add-requirements.txt`, optionally specify your requirements.txt files and `--dev` for dev dependencies.\n\n`poeareq` is provided is an alias to `poetry-add-requirements.txt`.\n\n```\n$ poeareq --help\n\nusage: poeareq [-h] [-D] [requirements.txt files ...]\n\nAdd dependencies specified in requirements.txt to your Poetry project\n\npositional arguments:\n  requirements.txt file(s)\n                        Path(s) to your requirements.txt file(s) (default: requirements.txt)\n\noptions:\n  -h, --help            show this help message and exit\n  -D, --dev             Add to development dependencies (default: False)\n```\n\n\n## Develop\n\n```\n$ git clone https://github.com/tddschn/poetry-add-requirements.txt.git\n$ cd poetry-add-requirements.txt\n$ poetry install\n```',
    'author': 'Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tddschn/poetry-add-requirements.txt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
