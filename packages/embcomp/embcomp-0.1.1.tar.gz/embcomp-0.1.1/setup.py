# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['embcomp']

package_data = \
{'': ['*']}

install_requires = \
['torch']

setup_kwargs = {
    'name': 'embcomp',
    'version': '0.1.1',
    'description': 'Composition of embeddings',
    'long_description': None,
    'author': 'Damien Sileo',
    'author_email': 'damien.sileo@kuleuven.be',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
