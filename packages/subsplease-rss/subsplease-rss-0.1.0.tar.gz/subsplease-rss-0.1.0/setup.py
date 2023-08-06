# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['subsplease_rss']

package_data = \
{'': ['*']}

install_requires = \
['feedparser>=6.0.10,<7.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'subsplease-rss',
    'version': '0.1.0',
    'description': 'SubsPlease RSS Helper',
    'long_description': None,
    'author': 'SlavWolf',
    'author_email': 'git@slavwolf.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
