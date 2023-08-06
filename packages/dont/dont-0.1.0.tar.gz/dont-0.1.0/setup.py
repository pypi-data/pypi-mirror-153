# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['dont']
setup_kwargs = {
    'name': 'dont',
    'version': '0.1.0',
    'description': 'Context manager base class that allows customizing execution of the contents',
    'long_description': None,
    'author': 'L3viathan',
    'author_email': 'git@l3vi.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
