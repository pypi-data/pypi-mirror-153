# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gpq']

package_data = \
{'': ['*']}

install_requires = \
['longprocess>=0.2.2,<0.3.0',
 'nvsmi>=0.4.2,<0.5.0',
 'persistQueue>=0.1.6,<0.2.0',
 'torch>=1.11.0,<2.0.0']

setup_kwargs = {
    'name': 'gpq',
    'version': '0.1.0',
    'description': '',
    'long_description': '# `gpq`\n\n```\n\n\n```\n',
    'author': 'yohan-pg',
    'author_email': 'pg.yohan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
