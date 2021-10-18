from sqlalchemy.orm import Session
from typing import List

import models
import schemas


def get_share_all(db: Session) -> List[models.Share]:
    return db.query(models.Share).filter().all()


def create_share(db: Session, share: schemas.ShareTotal, company_id: int):
    db_share = models.Share(**share.dict(), company_id=company_id)
    db.add(db_share)
    db.commit()
    db.refresh(db_share)
    return db_share
