# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tests', 'traderclient']

package_data = \
{'': ['*'], 'tests': ['data/*']}

install_requires = \
['arrow>=1.2.2,<2.0.0',
 'fire>=0.4.0,<0.5.0',
 'httpx>=0.16,<0.17',
 'numpy>=1.22.4,<2.0.0']

extras_require = \
{'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0'],
 'doc': ['mkdocs>=1.2.3,<2.0.0',
         'mkdocs-include-markdown-plugin>=3.2.3,<4.0.0',
         'mkdocs-material>=8.1.11,<9.0.0',
         'mkdocstrings>=0.18.0,<0.19.0',
         'mkdocs-autorefs>=0.4.1,<0.5.0',
         'livereload>=2.6.3,<3.0.0',
         'mike>=1.1.2,<2.0.0'],
 'test': ['black>=22.3.0,<23.0.0',
          'isort==5.6.4',
          'flake8==3.8.4',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'pytest==6.1.2',
          'pytest-cov==2.10.1',
          'sanic>=22.3.2,<23.0.0']}

entry_points = \
{'console_scripts': ['bt = traderclient.cli:main']}

setup_kwargs = {
    'name': 'zillionare-trader-client',
    'version': '0.3.9',
    'description': 'Zillionare Trader Client',
    'long_description': '# 大富翁交易客户端\n\ntrade-client是大富翁量化框架中用来交易的客户端。它对回测和实盘提供了几乎相同的接口，从而使得经过回测的策略，可以无缝切换到实盘环境中。\n\n## 功能\n\n* 进行实盘和回测交易\n* 获取账号基本信息，比如本金、资产、持仓、盈亏及盈亏比等。\n* 交易函数，比如买入（限价和市价）、卖出（限价和市价）、撤单等\n* 查询委托、成交、持仓（当日和指定日期）\n* 查询一段时间内的账户评估指标，比如sharpe, sortino, calmar, voliality, win rate, max drawdown等。\n* 查询参照标的同期指标。\n\n!!!Warning\n    在回测模式下，注意可能引起账户数据改变的操作，比如`buy`、`sell`等，必须严格按时间顺序执行，比如下面的例子：\n    ```\n    client.buy(..., order_time=datetime.datetime(2022, 3, 1, 9, 31))\n    client.buy(..., order_time=datetime.datetime(2022, 3, 4, 14, 31))\n    client.buy(..., order_time=datetime.datetime(2022, 3, 4, 14, 32))\n    client.sell(..., order_time=datetime.datetime(2022, 3, 7, 9, 31))\n    ```\n    是正确的执行顺序，但下面的执行顺序必然产生错误的结果(实际上服务器也会进行检测并报错误)\n    ```\n    client.buy(..., order_time=datetime.datetime(2022, 3, 1, 14, 31))\n    client.buy(..., order_time=datetime.datetime(2022, 3, 1, 9, 31))\n    client.sell(..., order_time=datetime.datetime(2022, 3, 7, 9, 31))\n    ```\n    策略需要自行决定是否允许这样的情况发生，以及如果发生失，会产生什么样的后果。\n\n## Credits\n\nThis package was created with [zillionare/python project wizard](https://zillionare.github.io/python-project-wizard) project template.\n',
    'author': 'Aaron Yang',
    'author_email': 'code@jieyu.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zillionare/trader-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
