from pydantic import BaseModel


class Request(BaseModel):
    cmd: str
    params: dict  # type: ignore
    nonce: int


class RequestV1(Request):
    sig: str


class RequestV2(Request):
    apiKey: str
