from sqlalchemy.orm import Session
from typing import List

import models
import schemas

from sqlalchemy import case, func
from schemas import TypeAction

case_quantity_for_type_action = case(
    [
        (models.Share.type_action == TypeAction.sell, models.Share.quantity * -1),
        (models.Share.type_action == TypeAction.buy, models.Share.quantity)
    ]
)


def get_share_all(db: Session) -> List[models.Share]:
    return db.query(models.Share).filter().all()


def get_quantity_for_type_action(db: Session, company_id: int) -> int:
    return db.query(
        func.sum(case_quantity_for_type_action)
    ).filter(models.Share.company_id == company_id).one()[0]


def create_share(db: Session, share: schemas.ShareTotal, company_id: int):
    quantity_actually = get_quantity_for_type_action(db, company_id)
    if share.type_action == TypeAction.sell:
        if quantity_actually - share.quantity < 0:
            return None
    db_share = models.Share(**share.dict(), company_id=company_id)
    db.add(db_share)
    db.commit()
    db.refresh(db_share)
    return db_share
