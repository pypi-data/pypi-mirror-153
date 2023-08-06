# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webvpn', 'webvpn.gateway']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'aiorun>=2022.4.1,<2023.0.0',
 'beautifulsoup4>=4.11.1,<5.0.0',
 'dynaconf>=3.1.8,<4.0.0',
 'sentry-sdk>=1.5.12,<2.0.0',
 'shellingham>=1.4.0,<2.0.0',
 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['webvpn = webvpn.cmd:app']}

setup_kwargs = {
    'name': 'webvpn',
    'version': '0.1.1',
    'description': 'TCP over WebVPN',
    'long_description': None,
    'author': 'Ming Yang',
    'author_email': 'ymviv@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
