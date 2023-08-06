# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['many_more_routes']

package_data = \
{'': ['*']}

install_requires = \
['getting-and-setting>=0.3.19,<0.4.0',
 'openpyxl>=3.0.9,<4.0.0',
 'pandas>=1.4.2,<2.0.0',
 'pandera>=0.11.0,<0.12.0']

setup_kwargs = {
    'name': 'many-more-routes',
    'version': '0.1.1',
    'description': 'Routing tools for the More project',
    'long_description': None,
    'author': 'Kim TImothy Engh',
    'author_email': 'kimothy@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
