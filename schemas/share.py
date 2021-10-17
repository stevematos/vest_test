from typing import List, Optional

from pydantic import BaseModel


class ShareBase(BaseModel):
    quantity: int
    price_unit: float


class ShareCreate(ShareBase):
    pass


class Share(ShareBase):
    id: int
    company_id: int

    class Config:
        orm_mode = True
