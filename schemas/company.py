from typing import List

from pydantic import BaseModel
from .share import Share


class CompanyBase(BaseModel):
    name: str
    symbol: str


class CompanyInput(CompanyBase):
    pass


class Company(CompanyBase):
    id: int
    shares: List[Share] = []

    class Config:
        orm_mode = True
