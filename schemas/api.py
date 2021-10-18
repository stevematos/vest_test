from pydantic import BaseModel
from typing import Dict


class ActionWithShare(BaseModel):
    quantity: int
    price_unit: str
    type_action: str
    company: str
    symbol_company: str


class ResponseModelBase(BaseModel):
    message: str
    data: BaseModel


class ActionWithShareResponseModel(ResponseModelBase):
    data: ActionWithShare
