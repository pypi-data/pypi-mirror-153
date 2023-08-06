# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['async_selective_queue']
setup_kwargs = {
    'name': 'async-selective-queue',
    'version': '0.1.0.post0',
    'description': 'Async queue with selective retrieval',
    'long_description': '# Async Selective Queue\n\n[![PyPI](https://img.shields.io/pypi/v/async-selective-queue)](https://pypi.org/project/async-selective-queue/)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/async-selective-queue)\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/dbluhm/async-selective-queue/Tests?label=tests)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n\nPython library for an asynchronous queue with the ability to selectively\nretrieve elements from the queue.\n',
    'author': 'Daniel Bluhm',
    'author_email': 'dbluhm@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dbluhm/async-selective-queue',
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
