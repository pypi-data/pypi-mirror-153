# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tradernet_api', 'tradernet_api.commands', 'tradernet_api.models']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.1,<2.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'tradernet-api',
    'version': '1.0.0',
    'description': 'Public API client for working with the Tradernet platform.',
    'long_description': '<div align="center">\n\n[![Upload Python Package](https://github.com/kutsevol/tradernet-api/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/kutsevol/tradernet-api/actions/workflows/build.yml)\n[![Python Version](https://img.shields.io/pypi/pyversions/tradernet_api.svg)](https://pypi.org/project/tradernet_api/)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/tradernet-api/tradernet_api/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/tradernet-api/tradernet_api/blob/master/.pre-commit-config.yaml)\n[![Semantic Versions](https://img.shields.io/badge/semantic--versions-python-e10079.svg)](https://github.com/kutsevol/tradernet-api/releases)\n[![License](https://img.shields.io/github/license/kutsevol/tradernet-api)](https://github.com/kutsevol/tradernet-api/blob/main/LICENSE)\n![Coverage Report](assets/images/coverage.svg)\n</div>\n\n# Tradernet API\nPublic API client for working with the Tradernet platform. </br>\n[Official API documentation](https://tradernet.com/tradernet-api)\n\n## Installation\n\n### Install package\n\n```bash\npip install -U tradernet-api\n```\n\nor \n\n```bash\npoetry add tradernet-api@latest\n```\n\n### Getting Started\n\n```python\nfrom tradernet_api.api import API\n\n# Setup client\napi_client = API(api_key="YOUR API KEY", secret_key="YOUR SECRET KEY")\n\n# Get only active orders by default\napi_client.get_orders()\n\n# Get all orders\napi_client.get_orders(active_only=False)\n\n# Get ticker info\napi_client.get_ticker_info(ticker="AAPL")\n\n# Send order to the platform\napi_client.send_order(ticker="AAPL", action=1, order_type=1, count=1, order_exp=1, limit_price=1, stop_price=1)\n\n# Delete/cancel active order\napi_client.delete_order(order_id=123456789)\n\n# Set stop loss and/or take profit\napi_client.set_stop_order(ticker="AAPL", stop_loss=1, take_profit=2)\n```\n\n## 🛡 License\n\n[![License](https://img.shields.io/github/license/kutsevol/tradernet-api)](https://github.com/kutsevol/tradernet-api/blob/main/LICENSE)\n\nThis project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/kutsevol/tradernet-api/blob/main/LICENSE) for more details.\n',
    'author': 'Artur Kutsevol',
    'author_email': 'arthur.kutsevol@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
