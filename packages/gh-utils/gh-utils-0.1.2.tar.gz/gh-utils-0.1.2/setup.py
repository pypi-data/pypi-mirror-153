# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gh_utils']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['ghcrar = gh_utils.gh_create_repo_and_add_to_remote:main']}

setup_kwargs = {
    'name': 'gh-utils',
    'version': '0.1.2',
    'description': 'GitHub CLI Utilities',
    'long_description': '',
    'author': 'Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tddschn/gh-utils',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
