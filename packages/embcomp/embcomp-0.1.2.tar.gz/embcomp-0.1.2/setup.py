# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['embcomp']
install_requires = \
['torch']

setup_kwargs = {
    'name': 'embcomp',
    'version': '0.1.2',
    'description': 'Composition of embeddings',
    'long_description': None,
    'author': 'Damien Sileo',
    'author_email': 'damien.sileo@kuleuven.be',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
