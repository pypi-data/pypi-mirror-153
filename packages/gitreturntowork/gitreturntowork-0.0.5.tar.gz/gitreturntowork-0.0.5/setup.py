# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gitreturntowork']

package_data = \
{'': ['*']}

install_requires = \
['PyInquirer>=1.0.3,<2.0.0']

setup_kwargs = {
    'name': 'gitreturntowork',
    'version': '0.0.5',
    'description': '',
    'long_description': None,
    'author': 'Brighten Tompkins',
    'author_email': 'brightenqtompkins@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
