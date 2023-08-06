# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djackal',
 'djackal.fields',
 'djackal.management',
 'djackal.management.commands',
 'djackal.model_mixins',
 'djackal.storage',
 'djackal.storage.migrations',
 'djackal.views']

package_data = \
{'': ['*']}

install_requires = \
['djangorestframework>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'djackal',
    'version': '0.0.1.dev39',
    'description': 'extension of Django REST Framework',
    'long_description': '# Djackal, Django Rest Framework extension\n\n[![version badge](https://badge.fury.io/py/djackal.svg)](https://badge.fury.io/py/djackal)\n\n![djackal image](https://imgur.com/XnlU8T9.jpg)\n\n**Djackal** is extension of Django REST Framework(DRF)\nthat help you easily implement the necessary features on your web backend server.\n\n\n## Warning\n\nThis repository is on developing. Some bugs may exist, possible to change suddenly. And no document yet.\n\n\n## Installation\n\n    pip install djackal\n',
    'author': 'jrog',
    'author_email': 'jrog612@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jrog612/djackal',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
