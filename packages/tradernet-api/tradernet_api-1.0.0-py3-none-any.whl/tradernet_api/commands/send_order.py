from typing import Any

from tradernet_api.models.order_model import Order


def send_order(
    self: Any,
    ticker: str,
    action: int,
    order_type: int,
    count: int,
    order_exp: int,
    limit_price: float | None = 0,
    stop_price: float | None = 0,
) -> Any:
    """
    A method that allows you to work with the submission of orders for execution.
    https://tradernet.com/tradernet-api/orders-send

    :param self: binds with API class
    :param ticker: Ticker name for execution
    :param action: Action: 1 - A Purchase (Buy); 2 - A Purchase when making trades with margin (Buy on Margin);
        3 - A Sale (Sell); 4 - A Sale when making trades with margin (Sell Short)
    :param order_type: Type of order: 1 - Market Order (Market); 2 - Order at a set price (Limit);
        3 - Market Stop-order (Stop); 4 - Stop-order at a set price (Stop Limit)
    :param count: Quantity in the order
    :param order_exp: Order expiration: 1 - Order "until the end of the current trading session" (Day);
        2 - Order "day/night or night/day" (Day + Ext);
        3 - Order "before cancellation" (GTC, before cancellation with participation in night sessions)
    :param limit_price: Price for limit order (optional)
    :param stop_price: Price for stop order (optional)

    :return: Response
    """
    command_name = "putTradeOrder"

    order_param = Order(
        instr_name=f"{ticker}.US".upper(),
        action_id=action,
        order_type_id=order_type,
        qty=count,
        limit_price=limit_price,
        stop_price=stop_price,
        expiration_id=order_exp,
    )

    return self._client_v2.send_request(command=command_name, params=order_param.dict())
