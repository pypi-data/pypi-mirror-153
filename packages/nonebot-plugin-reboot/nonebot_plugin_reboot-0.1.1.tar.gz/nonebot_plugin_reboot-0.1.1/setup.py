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
    'version': '0.1.1',
    'description': 'Reboot your bot by using command',
    'long_description': '# Nonebot-plugin-reboot \n用命令重启 bot \n\n\n## 注意事项\n**不支持** `nb-cli`，即 `nb run` 启动方式。\n需要在 bot 目录下使用 `python bot.py` 启动。\n\n仅在 `linux` `python3.8` `fastapi` 驱动器下测试过。\n理论上与平台无关，但是我没测试（\n\n\n## 安装\n通过 pip 安装:\n`pip install nonebot-plugin-reboot`  \n并加载插件\n\n\n## 使用\n**超级用户**向机器人**私聊**发送**命令** `重启`, `reboot` 或 `restart`  \n注意命令 `COMMAND_START`.\n\n\n## 配置项 \n`reboot_load_command`: `bool` \n- 加载内置的 `onebot v11` 重启命令 \n- 可以通过命令 `重启` `reboot` `restart` 触发重启 \n- 默认值: `True` \n\n\n## 用程序触发重启\n```python\nfrom nonebot_plugin_reboot import Reloader\nReloader.reload()\n```\n\n\n## 依赖 \n`nonebot2 >= 2.0.0beta.2` ',
    'author': '18870',
    'author_email': 'a20110123@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/18870/nonebot-plugin-reboot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
