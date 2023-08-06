# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot', 'nonebot.adapters.mirai2', 'nonebot.adapters.mirai2.event']

package_data = \
{'': ['*']}

install_requires = \
['nonebot2>=2.0.0b1']

setup_kwargs = {
    'name': 'nonebot-adapter-mirai2',
    'version': '0.0.12',
    'description': '兼容 MiraiApiHttp2.x 的 nonebot2_adapter',
    'long_description': None,
    'author': 'ieew',
    'author_email': 'i@ieew.cc',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0.0',
}


setup(**setup_kwargs)
