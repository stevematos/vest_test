from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db import Base


# todo: ver si la zona horaria afecta a la salida de la tabla

class Share(Base):
    __tablename__ = "share"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, index=True)
    symbol_currency = Column(String, index=True)
    price_unit = Column(Float, index=True)
    create_date = Column(DateTime(timezone=True), server_default=func.now())
    company_id = Column(Integer, ForeignKey("company.id"))

    company = relationship("Company", back_populates="shares")
