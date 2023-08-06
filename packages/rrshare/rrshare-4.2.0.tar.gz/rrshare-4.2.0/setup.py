# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rrshare',
 'rrshare.RQSetting',
 'rrshare.rqFactor',
 'rrshare.rqFetch',
 'rrshare.rqSU',
 'rrshare.rqUpdate',
 'rrshare.rqUtil',
 'rrshare.rqWeb',
 'rrshare.sql']

package_data = \
{'': ['*'], 'rrshare': ['templates/*'], 'rrshare.rqWeb': ['templates/*']}

install_requires = \
['click>=8.1.0,<9.0.0',
 'easyquotation>=0.7.5,<0.8.0',
 'tushare>=1.2.62,<2.0.0',
 'zenlog>=1.1,<2.0']

entry_points = \
{'console_scripts': ['rrshare = rrshare:entry_point']}

setup_kwargs = {
    'name': 'rrshare',
    'version': '4.2.0',
    'description': 'stock data(from tusharepro) & analysis',
    'long_description': None,
    'author': 'rome',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
