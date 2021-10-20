from pydantic import BaseModel
from schemas.general import TypeAction


class ShareBase(BaseModel):
    quantity: int


class ShareInput(ShareBase):
    pass


class ShareTotal(ShareBase):
    price_unit: float
    symbol_currency: str
    type_action: TypeAction


class Share(ShareTotal):
    id: int
    company_id: int

    class Config:
        orm_mode = True
