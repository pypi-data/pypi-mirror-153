from typing import Mapping, Optional, Union

import hashlib
import hmac
import time
from dataclasses import dataclass

from requests import Response

from tradernet_api.const import api_url
from tradernet_api.models.request_model import RequestV1, RequestV2
from tradernet_api.session import session


@dataclass
class Client:
    """
    Base class Client.
    """

    api_key: str
    secret_key: str

    def send_request(
        self, command: str, params: dict[str, str | dict[str, str]] | None = None
    ) -> Response:
        pass


class ClientV1(Client):
    def send_request(
        self, command: str, params: dict[str, str | dict[str, str]] | None = None
    ) -> Response:
        data = RequestV1(
            cmd=command,
            params=params,
            nonce=int(time.time() * 10000),
            sig=hmac.new(key=self.secret_key.encode(), digestmod="MD5").hexdigest(),
        )
        return session.post(api_url, data={"q": data.json()})


class ClientV2(Client):
    path: str = "/v2/cmd/{command}"

    def url_form_encoded(
        self, data: Mapping[str, str | int | dict[str, str]], root_name: str | None = ""
    ) -> str:
        """
        Encoded dictionary python format to url form with square brackets.

        :param data: data to be encoded
        :param root_name: custom root name for nested key in dictionary
        :return: str
        """
        result = []

        for key, value in sorted(data.items()):
            if isinstance(value, dict):
                result.append(self.url_form_encoded(value, key))
            else:
                result.append(
                    f"{root_name}[{key}]={value}" if root_name else f"{key}={value}"
                )
        return "&".join(result)

    def convert_to_query_string(self, data: Mapping[str, str | dict[str, str]]) -> str:
        """
        Unpack dictionary with nested keys in string

        :param data: data to be unpacked
        :return: str
        """
        result = []
        for key, value in sorted(data.items()):
            result.append(
                f"{key}={self.convert_to_query_string(value)}"
                if isinstance(value, dict)
                else f"{key}={value}"
            )
        return "&".join(result)

    def send_request(
        self, command: str, params: dict[str, str | dict[str, str]] | None = None
    ) -> Response:
        data = RequestV2(
            cmd=command,
            params=params,
            nonce=int(time.time() * 10000),
            apiKey=self.api_key,
        )
        headers = {
            "X-NtApi-Sig": hmac.new(
                key=self.secret_key.encode(),
                msg=self.convert_to_query_string(data.dict()).encode("utf-8"),
                digestmod=hashlib.sha256,
            ).hexdigest(),
            "Content-Type": "application/x-www-form-urlencoded",
        }

        url_query = self.url_form_encoded(data.dict())

        return session.post(
            f"{api_url}{self.path}", params=url_query, headers=headers, data=url_query
        )
