from sqlalchemy import Column, ForeignKey, Integer, Float, String
from sqlalchemy.orm import relationship

from db import Base


class Share(Base):
    __tablename__ = "share"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, index=True)
    price_unit = Column(Float, index=True)
    symbol_currency = Column(String, index=True)
    company_id = Column(Integer, ForeignKey("company.id"))

    company = relationship("Company", back_populates="shares")
