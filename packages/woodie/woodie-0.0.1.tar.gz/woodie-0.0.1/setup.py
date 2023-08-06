# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['woodie']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'woodie',
    'version': '0.0.1',
    'description': '',
    'long_description': '# WOODY',
    'author': 'limonyellow',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/limonyellow/woody',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
