# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alfort']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'alfort',
    'version': '0.1.7',
    'description': '',
    'long_description': 'None',
    'author': 'Masahiro Wada',
    'author_email': 'argon.argon.argon@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
