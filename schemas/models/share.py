from pydantic import BaseModel


class ShareBase(BaseModel):
    quantity: int


class ShareInput(ShareBase):
    pass


class ShareTotal(ShareBase):
    price_unit: float
    symbol_currency: str


class Share(ShareTotal):
    id: int
    company_id: int

    class Config:
        orm_mode = True
