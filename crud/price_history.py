from sqlalchemy.orm import Session
from typing import List

import models
import schemas


def get_price_history_by_symbol(db: Session, symbol: str) -> List[models.PriceHistory]:
    return db.query(models.PriceHistory).join(models.Company).filter(models.Company.symbol == symbol).all()


def create_price_history(db: Session, price_history: schemas.PriceHistoryTotal, company_id: int):
    db_price_history = models.PriceHistory(**price_history.dict(), company_id=company_id)
    db.add(db_price_history)
    db.commit()
    db.refresh(db_price_history)
    return db_price_history
