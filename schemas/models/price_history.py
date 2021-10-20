from pydantic import BaseModel
from schemas.general import TypeAction
from datetime import datetime


class PriceHistoryBase(BaseModel):
    price_unit: float
    symbol_currency: str


class PriceHistoryTotal(PriceHistoryBase):
    pass


class PriceHistory(PriceHistoryTotal):
    id: int
    company_id: int

    class Config:
        orm_mode = True
