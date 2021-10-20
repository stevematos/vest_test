from pydantic import BaseModel
from schemas.general import TypeAction
from datetime import datetime


class ActionWithShareResponseModel(BaseModel):
    quantity: int
    price_unit: str
    type_action: TypeAction
    company: str
    symbol_company: str



class PricesHistoryBySymbolResponseModel(BaseModel):
    price_unit: str
    create_date: datetime
