from typing import Any

from tradernet_api.models.order_model import Order


def get_orders(self: Any, active_only: bool | None = True) -> Any:
    """
    Receive orders in the current period and subscribe for changes.
    https://tradernet.com/tradernet-api/orders-get-current-history

    :param self: binds with API class
    :param active_only: 1/0 We show only active orders. Optional
    :return: Response
    """
    command_name = "getNotifyOrderJson"

    order_param = Order(active_only=active_only)

    return self._client_v2.send_request(command=command_name, params=order_param.dict())
