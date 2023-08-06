from typing import Optional

from pydantic import BaseModel


class Order(BaseModel):
    instr_name: Optional[str] = None
    ticker: Optional[str] = None
    action_id: Optional[int] = None
    order_type_id: Optional[int] = None
    qty: Optional[int] = None
    limit_price: Optional[float] = None
    stop_price: Optional[float] = None
    expiration_id: Optional[int] = None
    order_id: Optional[int] = None
    active_only: Optional[bool] = None
    sup: Optional[bool] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None


# class DeleteOrder(BaseModel):
#     order_id: str


# class GetOrder(BaseModel):
#     active_only: int


# class GetTickerInfo(BaseModel):
#     ticker: str
#     sup: bool


# class SetStopOrder(BaseModel):
#     instr_name: str
#     stop_loss: str
#     take_profit: str
