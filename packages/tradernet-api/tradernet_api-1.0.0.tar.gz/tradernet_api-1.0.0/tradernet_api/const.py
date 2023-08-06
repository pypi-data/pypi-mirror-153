from enum import Enum

api_url = "https://tradernet.ru/api"


class Command(Enum):
    send_order = "send_order"
    delete_order = "delete_order"
    get_orders = "get_orders"
    get_ticker_info = "get_ticker_info"
    set_stop_order = "set_stop_order"
