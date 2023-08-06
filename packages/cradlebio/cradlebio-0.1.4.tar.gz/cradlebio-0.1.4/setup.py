# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cradlebio']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.70,<2.0',
 'google-api-python-client>=2.42.0,<3.0.0',
 'google-auth>=2.6,<3.0',
 'google-cloud-firestore>=2.3,<3.0',
 'google-cloud-storage>=2.1,<3.0',
 'janus>=1.0,<2.0']

setup_kwargs = {
    'name': 'cradlebio',
    'version': '0.1.4',
    'description': "Client for Cradle's Alphafold-as-a-service",
    'long_description': None,
    'author': 'Eli Bixby',
    'author_email': 'eli@cradle.bio',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
