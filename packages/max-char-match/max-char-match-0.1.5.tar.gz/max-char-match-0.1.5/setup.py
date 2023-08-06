# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['max_char_match']

package_data = \
{'': ['*']}

install_requires = \
['datasets>=2.1.0,<3.0.0',
 'diff-match-patch>=20200713,<20200714',
 'more-itertools>=8.12.0,<9.0.0',
 'numpy>=1.22.3,<2.0.0',
 'tqdm>=4.64.0,<5.0.0']

setup_kwargs = {
    'name': 'max-char-match',
    'version': '0.1.5',
    'description': 'MaxCharMatch metric',
    'long_description': None,
    'author': 'melisa-writer',
    'author_email': 'melisa@writer.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
