from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


from db import Base
from models.share import Share
from models.price_history import PriceHistory


class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    symbol = Column(String, unique=True, index=True)

    shares = relationship(Share, back_populates="company")
    prices_history = relationship(PriceHistory, back_populates="company")
