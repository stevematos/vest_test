from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db import Base


class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    price_unit = Column(Float, index=True)
    symbol_currency = Column(String, index=True)
    create_date = Column(DateTime(timezone=True), server_default=func.now())
    company_id = Column(Integer, ForeignKey("company.id"))

    company = relationship("Company", back_populates="prices_history")
