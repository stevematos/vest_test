from sqlalchemy.orm import Session

import models
import schemas


def create_share(db: Session, share: schemas.ShareTotal, company_id: int):
    db_share = models.Share(**share.dict(), company_id=company_id)
    db.add(db_share)
    db.commit()
    db.refresh(db_share)
    return db_share
