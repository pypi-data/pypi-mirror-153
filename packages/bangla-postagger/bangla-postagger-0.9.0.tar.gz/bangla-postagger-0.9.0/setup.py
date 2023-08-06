# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bangla_postagger']

package_data = \
{'': ['*']}

install_requires = \
['deep-translator>=1.8.3,<2.0.0',
 'flair>=0.11.1,<0.12.0',
 'spacy>=3.3.0,<4.0.0',
 'textblob>=0.17.1,<0.18.0',
 'torch>=1.11.0,<2.0.0']

setup_kwargs = {
    'name': 'bangla-postagger',
    'version': '0.9.0',
    'description': 'A Bangla Parts of Speech Tagger using Bangla-English Alignment',
    'long_description': '# Bangla PoS Tagger\nA Bangla Parts of Speech Tagger using Bangla-English Alignment',
    'author': 'Md. Musfiqur Rahaman',
    'author_email': 'musfiqur.rahaman@northsouth.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MusfiqDehan/bangla-postagger',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
