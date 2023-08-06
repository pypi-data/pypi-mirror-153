# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_r3nzskin']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.1.1,<10.0.0',
 'httpx>=0.23.0,<0.24.0',
 'nonebot-adapter-onebot>=2.1.0,<3.0.0',
 'nonebot-plugin-apscheduler>=0.1.2,<0.2.0']

setup_kwargs = {
    'name': 'nonebot-plugin-r3nzskin',
    'version': '0.1.1',
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
