# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bridgebots_sequence']

package_data = \
{'': ['*'],
 'bridgebots_sequence': ['drive/MyDrive/bid_learn/models/target_bidding/run_1_checkpoints/*',
                         'drive/MyDrive/bid_learn/models/target_bidding/run_1_checkpoints/variables/*']}

install_requires = \
['bridgebots>=0.0.10,<0.0.11']

extras_require = \
{'tf': ['tensorflow>=2.8.0,<3.0.0'],
 'tf_macos': ['tensorflow_macos>=2.8.0,<3.0.0']}

setup_kwargs = {
    'name': 'bridgebots-sequence',
    'version': '0.0.1.dev0',
    'description': 'Sequence models for Contract Bridge',
    'long_description': None,
    'author': 'Forrest Rice',
    'author_email': 'forrest.d.rice@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
