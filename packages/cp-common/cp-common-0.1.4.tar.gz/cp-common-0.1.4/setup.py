# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cp_common', 'cp_common.scheduler', 'cp_common.scheduler.protos']

package_data = \
{'': ['*']}

install_requires = \
['APScheduler>=3.9.1,<4.0.0',
 'celery>=5.2.7,<6.0.0',
 'grpcio-tools>=1.46.3,<2.0.0',
 'grpcio>=1.46.3,<2.0.0',
 'httpx>=0.23.0,<0.24.0',
 'loguru>=0.6.0,<0.7.0',
 'redis>=4.3.1,<5.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=12.4.4,<13.0.0',
 'sanic>=22.3.2,<23.0.0']

setup_kwargs = {
    'name': 'cp-common',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'zmf963',
    'author_email': 'zmf96@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
