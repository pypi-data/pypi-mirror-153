# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_warframe_clock']

package_data = \
{'': ['*'], 'nonebot_plugin_warframe_clock': ['data/*']}

install_requires = \
['Pillow>=9.1.1,<10.0.0',
 'arrow>=1.2.2,<2.0.0',
 'httpx>=0.23.0,<0.24.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot2==2.0.0b3']

setup_kwargs = {
    'name': 'nonebot-plugin-warframe-clock',
    'version': '1.3',
    'description': 'nonebot2插件，查询Warframe开放地图时间。',
    'long_description': '<p align="center">\n\t<a href="https://github.com/axStar/WarframeQQbot_RemiliaScarlet">\n\t\t<img src="https://s3.bmp.ovh/imgs/2022/05/26/c0293edb48a8333f.png" width="200" height="200" alt="Remilia·Scarlet">\n\t</a>\n</p>\n<div align="center">\n\n# Nonebot2-Plugin-WarframeClock\n\n**❤基于[NoneBot2](https://github.com/nonebot/nonebot2)实现，用以实现Warframe各个地图的时间查询。❤**\n\n<p align="center">\n\t<a href="https://space.bilibili.com/100455457">\n\t\t<img src="https://img.shields.io/badge/B%E7%AB%99-white?logo=bilibili">\n\t</a>\n\t<a href="https://qm.qq.com/cgi-bin/qm/qr?k=a1sMkSIXA_F2_6tDhuXdnD2u7ibinIcT&noverify=0">\n\t\t<img src="https://img.shields.io/badge/QQ-%23339999?logo=Tencent%20QQ">\n\t</a>\n\t<img src="https://img.shields.io/badge/%E5%BC%80%E5%8F%91%E8%BF%9B%E5%BA%A6-100%25-red">\n</p>\n</div>\n\n# 安装\n使用pip：\n```\npip install nonebot-plugin-warframe-clock\n```\n>pip安装完成后需要手动加载。\n>1. 在bot.py中添加： \n```\nnonebot.load_plugin("nonebot_plugin_warframe_clock")\n```\n>2. 在pyproject.toml中添加：\n```\n[tool.nonebot]\nplugins = ["nonebot_plugin_warframe_clock"]\n```\n\n# 功能\n<details>\n<summary>夜灵平野</summary>\n<img src = \'https://i.bmp.ovh/imgs/2022/05/30/89e81aa3d5abd11e.png\' />\n</details>\n\n<details>\n<summary>地球</summary>\n<img src = \'https://s3.bmp.ovh/imgs/2022/05/30/e9160c5475eadcb1.png\' />\n</details>\n\n<details>\n<summary>奥布山谷</summary>\n<img src = \'https://s3.bmp.ovh/imgs/2022/05/30/f814ad9b154863de.png\' />\n</details>\n\n<details>\n<summary>魔胎之境</summary>\n<img src = \'https://s3.bmp.ovh/imgs/2022/05/30/88c53e7bb3783319.png\' />\n</details>\n',
    'author': 'Aa',
    'author_email': '2272613209@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
