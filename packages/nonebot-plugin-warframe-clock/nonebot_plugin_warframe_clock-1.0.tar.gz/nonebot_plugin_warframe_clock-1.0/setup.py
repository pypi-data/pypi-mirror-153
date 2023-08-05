# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_warframe_clock']

package_data = \
{'': ['*'], 'nonebot_plugin_warframe_clock': ['data/*']}

install_requires = \
['Pillow>=9.1.1,<10.0.0',
 'nb-cli>=0.6.7,<0.7.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-warframe-clock',
    'version': '1.0',
    'description': '',
    'long_description': None,
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
