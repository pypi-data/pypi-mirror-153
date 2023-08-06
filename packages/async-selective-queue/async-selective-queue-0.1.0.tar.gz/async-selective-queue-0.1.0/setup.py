# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['async_selective_queue']
setup_kwargs = {
    'name': 'async-selective-queue',
    'version': '0.1.0',
    'description': 'Async queue with selective retrieval',
    'long_description': None,
    'author': 'Daniel Bluhm',
    'author_email': 'dbluhm@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
