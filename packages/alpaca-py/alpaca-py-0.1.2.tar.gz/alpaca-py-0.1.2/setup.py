# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alpaca',
 'alpaca.broker',
 'alpaca.broker.models',
 'alpaca.common',
 'alpaca.common.models',
 'alpaca.data',
 'alpaca.trading',
 'alpaca.trading.models']

package_data = \
{'': ['*']}

install_requires = \
['msgpack>=1.0.3,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'websockets>=10.2,<11.0']

setup_kwargs = {
    'name': 'alpaca-py',
    'version': '0.1.2',
    'description': 'The new official Python SDK for the https://alpaca.markets/ API',
    'long_description': '# AlpacaPy\n\n[![Downloads](https://pepy.tech/badge/alpaca-py/month)](https://pepy.tech/project/alpaca-py)\n\n### Dev setup\n\nThis project is managed via poetry so setup should be just running `poetry install`.\n\nThis repo is using [`pre-commit`](https://pre-commit.com/) to setup some checks to happen at commit time to keep the\nrepo clean. To set these up after you\'ve run `poetry install` just run `poetry run pre-commit install` to have\npre-commit setup these hooks\n\n**Note: AlpacaPy is in the very early stages of alpha development and is not production ready. Currently AlpacaPy\ninterfaces with only the Market Data API, however the other APIs are coming soon.**\n\n## Basic Example Use Cases\n\n**Requesting Historical Market Data**\n\nTo retrieve historical market data, you’ll need to instantiate a historical data client with your API keys. There are\nmany different methods that allow you to access various stock and crypto data. To see the full range of data types\navailable, read the [API reference for market data](https://alpaca.markets/docs/python-sdk/api_reference/data_api.html).\n\nIn this example, we will query daily bar data for Apple Inc (AAPL) between January 1st 2021 and December 31st 2021. Then\nwe will convert the data to a dataframe and print it out to the console.\n\n```python\nfrom alpaca.data.historical import HistoricalDataClient\nfrom alpaca.common.time import TimeFrame\n\nAPI_KEY = \'api-key\'\nSECRET_KEY = \'secret-key\'\n\nclient = HistoricalDataClient(API_KEY, SECRET_KEY)\n\nbars = client.get_bars("AAPL", TimeFrame.Day, "2021-01-01", "2021-12-31")\n\nprint(bars.df)\n\n#             open      high      low   close     volume  trade_count        vwap\n# timestamp\n# 2021-01-04  133.56  133.6116  126.760  129.41  143302687      1310228  129.732580\n# 2021-01-05  128.98  131.7400  128.430  131.01   97667342       707584  130.717944\n# 2021-01-06  127.53  131.0499  126.382  126.60  155104120      1202580  128.350036\n# 2021-01-07  128.38  131.6300  127.860  130.92  109581117       718363  130.153889\n# 2021-01-08  132.50  132.6300  130.230  132.05  105158675       800071  131.565744\n# ...            ...       ...      ...     ...        ...          ...         ...\n# 2021-12-27  177.10  180.4200  177.070  180.33   74912939       629431  179.056944\n# 2021-12-28  180.20  181.3300  178.530  179.29   79103863       631316  179.707003\n# 2021-12-29  179.30  180.6300  178.140  179.38   62325973       491576  179.455692\n# 2021-12-30  179.59  180.5700  178.090  178.20   59770632       498613  179.374495\n# 2021-12-31  178.00  179.2300  177.260  177.57   64038680       451478  177.800285\n\n# [252 rows x 7 columns]\n```\n\n**Subscribing to Live Market Data**\n\nLive market data is available for both crypto and stocks via websocket interfaces. Keep in mind live stock data is only\navailable during market hours on trading days, whereas live crypto data is available 24/7. In this example, we will\nsubscribe to live quote data for Bitcoin (BTCUSD). To do so, first we will need to create an instance of the\nCryptoDataStream client with our API keys. Then we can create an asynchronous callback method to handle our live data as\nit is available.\n\n```python\nfrom alpaca.data.live import CryptoDataStream\n\nAPI_KEY = \'api-key\'\nSECRET_KEY = \'secret-key\'\n\nclient = CryptoDataStream(API_KEY, SECRET_KEY)\n\n\n# handler function will receive data as the data arrives\nasync def handler(data):\n    print(data)\n\n\n# subscribe to quote data for BTCUSD\nclient.subscribe_quotes(handler, "BTCUSD")\n\n# start websocket client\nclient.run()\n```\n',
    'author': 'Rahul Chowdhury',
    'author_email': 'rahul.chowdhury@alpaca.markets',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alpacahq/alpaca-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
