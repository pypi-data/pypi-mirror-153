# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_xtra_info']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'flask-xtra-info',
    'version': '0.3.10',
    'description': 'Inject extra info into flask headers and logs',
    'long_description': None,
    'author': 'jthop',
    'author_email': 'jh@mode14.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
