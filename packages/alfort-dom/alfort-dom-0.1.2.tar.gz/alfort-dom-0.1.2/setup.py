# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alfort_dom']

package_data = \
{'': ['*']}

install_requires = \
['alfort>=0.1.8,<0.2.0']

setup_kwargs = {
    'name': 'alfort-dom',
    'version': '0.1.2',
    'description': '',
    'long_description': 'None',
    'author': 'Masahiro Wada',
    'author_email': 'argon.argon.argon@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
