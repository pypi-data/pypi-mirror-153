# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uw_it', 'uw_it.flask_util']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'uw-it-flask-gunicorn-json-logger',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Tom Thorogood',
    'author_email': 'tom@tomthorogood.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
