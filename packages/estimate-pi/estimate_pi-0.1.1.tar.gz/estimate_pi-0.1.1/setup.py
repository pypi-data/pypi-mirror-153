# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['estimate_pi']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.2,<4.0.0', 'numpy>=1.22.4,<2.0.0']

setup_kwargs = {
    'name': 'estimate-pi',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Chang-Goo Kim',
    'author_email': 'changgoo@princeton.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
