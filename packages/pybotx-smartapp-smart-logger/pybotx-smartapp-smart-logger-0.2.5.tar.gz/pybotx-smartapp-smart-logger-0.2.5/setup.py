# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybotx_smartapp_smart_logger']

package_data = \
{'': ['*']}

install_requires = \
['pybotx-smart-logger>=0.6.7,<0.8.0',
 'pybotx-smartapp-rpc>=0.4.1,<0.5.0',
 'pybotx>=0.42.0,<0.45.0']

setup_kwargs = {
    'name': 'pybotx-smartapp-smart-logger',
    'version': '0.2.5',
    'description': '',
    'long_description': None,
    'author': 'Arseniy Zhiltsov',
    'author_email': 'arseniy.zhiltsov@ccsteam.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
