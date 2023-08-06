# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_reboot']

package_data = \
{'': ['*']}

install_requires = \
['nonebot2>=2.0.0-beta.2,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-reboot',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': '18870',
    'author_email': 'a20110123@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
