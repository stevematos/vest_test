from sqlalchemy.orm import Session
from typing import List

import models
import schemas


def get_company_all(db: Session) -> List[models.Company]:
    return db.query(models.Company).filter().all()


def get_company_by_symbol(db: Session, symbol: str):
    return db.query(models.Company).filter(models.Company.symbol == symbol).first()


def get_company_or_create(db: Session, company: schemas.CompanyInput):
    company_check = get_company_by_symbol(db, company.symbol)
    if company_check:
        db_company = company_check
    else:
        db_company = models.Company(**company.dict())
        db.add(db_company)
        db.commit()
        db.refresh(db_company)
    return db_company
