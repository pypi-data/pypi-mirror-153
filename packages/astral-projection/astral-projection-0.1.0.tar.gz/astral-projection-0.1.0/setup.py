# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['astral_projection']
install_requires = \
['colorful>=0.5.4,<0.6.0', 'dont>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'astral-projection',
    'version': '0.1.0',
    'description': 'Run code inside a context manager on a remote machine',
    'long_description': None,
    'author': 'L3viathan',
    'author_email': 'git@l3vi.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
