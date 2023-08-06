# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytorch_extra_mhirano',
 'pytorch_extra_mhirano.experimental',
 'pytorch_extra_mhirano.nn']

package_data = \
{'': ['*']}

install_requires = \
['torch>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'pytorch-extra-mhirano',
    'version': '0.1.6',
    'description': '',
    'long_description': None,
    'author': 'Masanori HIRANO',
    'author_email': 'masa.hirano.1996@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
