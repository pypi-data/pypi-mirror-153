# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_does_huey']

package_data = \
{'': ['*']}

install_requires = \
['huey>=2.4.3,<3.0.0']

setup_kwargs = {
    'name': 'flask-does-huey',
    'version': '0.5.4',
    'description': 'Flask extension to use huey task queues',
    'long_description': None,
    'author': 'jthop',
    'author_email': 'jh@mode14.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
