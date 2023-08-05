# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['hier_config']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4']

setup_kwargs = {
    'name': 'hier-config',
    'version': '2.2.2',
    'description': 'A network configuration comparison tool, used to build remediation configurations.',
    'long_description': None,
    'author': 'Andrew Edwards',
    'author_email': 'edwards.andrew@heb.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
