<div align="center">

[![Upload Python Package](https://github.com/kutsevol/tradernet-api/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/kutsevol/tradernet-api/actions/workflows/build.yml)
[![Python Version](https://img.shields.io/pypi/pyversions/tradernet_api.svg)](https://pypi.org/project/tradernet_api/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/tradernet-api/tradernet_api/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/tradernet-api/tradernet_api/blob/master/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/semantic--versions-python-e10079.svg)](https://github.com/kutsevol/tradernet-api/releases)
[![License](https://img.shields.io/github/license/kutsevol/tradernet-api)](https://github.com/kutsevol/tradernet-api/blob/main/LICENSE)
![Coverage Report](assets/images/coverage.svg)
</div>

# Tradernet API
Public API client for working with the Tradernet platform. </br>
[Official API documentation](https://tradernet.com/tradernet-api)

## Installation

### Install package

```bash
pip install -U tradernet-api
```

or 

```bash
poetry add tradernet-api@latest
```

### Getting Started

```python
from tradernet_api.api import API

# Setup client
api_client = API(api_key="YOUR API KEY", secret_key="YOUR SECRET KEY")

# Get only active orders by default
api_client.get_orders()

# Get all orders
api_client.get_orders(active_only=False)

# Get ticker info
api_client.get_ticker_info(ticker="AAPL")

# Send order to the platform
api_client.send_order(ticker="AAPL", action=1, order_type=1, count=1, order_exp=1, limit_price=1, stop_price=1)

# Delete/cancel active order
api_client.delete_order(order_id=123456789)

# Set stop loss and/or take profit
api_client.set_stop_order(ticker="AAPL", stop_loss=1, take_profit=2)
```

## 🛡 License

[![License](https://img.shields.io/github/license/kutsevol/tradernet-api)](https://github.com/kutsevol/tradernet-api/blob/main/LICENSE)

This project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/kutsevol/tradernet-api/blob/main/LICENSE) for more details.
