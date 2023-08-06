# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autoretouchlib', 'autoretouchlib.mock']

package_data = \
{'': ['*']}

install_requires = \
['canonicaljson>=1.3.0,<2.0.0',
 'fakeredis==1.6.1',
 'fastapi>=0.65.1',
 'google-cloud-storage>=1.42.3',
 'grpcio>=1.41.0',
 'opencensus-ext-stackdriver>=0.8.0',
 'opencensus>=0.7.13',
 'psutil>=5.8.0',
 'redis>=3.5.3,<4.0.0',
 'requests_mock>=1.8.0,<2.0.0']

setup_kwargs = {
    'name': 'autoretouch-service-library',
    'version': '2.1.1',
    'description': 'Autoretouch helper library',
    'long_description': None,
    'author': 'Till Lorentzen',
    'author_email': 'till@autoretouch.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
