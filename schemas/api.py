from pydantic import BaseModel
from schemas.general import TypeAction


class ActionWithShare(BaseModel):
    quantity: int
    price_unit: str
    type_action: TypeAction
    company: str
    symbol_company: str


class ResponseModelBase(BaseModel):
    message: str
    data: BaseModel


class ActionWithShareResponseModel(ResponseModelBase):
    data: ActionWithShare
