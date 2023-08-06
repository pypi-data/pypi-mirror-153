from dataclasses import dataclass

from tradernet_api.client import ClientV1, ClientV2
from tradernet_api.commands import (
    delete_order,
    get_orders,
    get_ticker_info,
    send_order,
    set_stop_order,
)
from tradernet_api.const import Command


@dataclass
class API:
    api_key: str
    secret_key: str

    def __post_init__(self):
        self._client_v1 = ClientV1(api_key=self.api_key, secret_key=self.secret_key)
        self._client_v2 = ClientV2(api_key=self.api_key, secret_key=self.secret_key)


for command in Command:
    setattr(API, command.name, globals()[command.name])
