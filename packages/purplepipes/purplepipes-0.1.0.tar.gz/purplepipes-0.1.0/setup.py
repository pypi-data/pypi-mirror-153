# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['purplepipes']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'purplepipes',
    'version': '0.1.0',
    'description': 'Pipes for data processing using pandas.',
    'long_description': '# :sparkles: 💜 Purple Pipes 💜 :sparkles:\n\nUses:\n- poetry\n- black\n- pep8\n- pre-commit\n- coverage\n\nWe assume that __all tests must pass__ and that - while test coverage is a poor single metric - its probably a bad idea to have it be under 60%.\n',
    'author': "J 'Indi' Harrington",
    'author_email': 'indigoharrington@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SentientHousePlant/purplepipes',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
