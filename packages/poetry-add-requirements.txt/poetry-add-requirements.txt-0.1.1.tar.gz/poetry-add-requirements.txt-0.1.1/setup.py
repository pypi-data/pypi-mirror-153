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
    'version': '0.1.1',
    'description': '',
    'long_description': '',
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
