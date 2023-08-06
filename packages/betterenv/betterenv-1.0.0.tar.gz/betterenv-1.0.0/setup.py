# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['betterenv']
setup_kwargs = {
    'name': 'betterenv',
    'version': '1.0.0',
    'description': 'A custom environment library',
    'long_description': None,
    'author': 'The Artful Bodger',
    'author_email': 'theartfulbodger@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
