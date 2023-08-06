from typing import Any

from tradernet_api.models.order_model import Order


def set_stop_order(
    self: Any,
    ticker: str,
    stop_loss: float | None = 0,
    take_profit: float | None = 0,
) -> Any:
    """
    Sending Stop Loss and Take Profit commands for execution.
    https://tradernet.com/tradernet-api/stop-loss

    :param self: binds with API class
    :param ticker: The instrument used to issue an order
    :param stop_loss: Stop Loss order price. Optional
    :param take_profit: Take profit order price. Optional

    :return: Response
    """
    command_name = "putStopLoss"

    order_param = Order(
        ticker=f"{ticker}.US".upper(), stop_loss=stop_loss, take_profit=take_profit
    )

    return self._client_v2.send_request(command=command_name, params=order_param.dict())
