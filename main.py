from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from enum import Enum

import crud
import schemas
from api import api
from db import SessionLocal, engine, Base
from utils import split_symbol_and_number

Base.metadata.create_all(bind=engine)


class TypeAction(str, Enum):
    buy = "buy"
    sell = "sell"


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/status")
async def root():
    return {"status": "ready"}


@app.post("/share/{symbol}/{type_action}")
async def action_with_share(symbol: str, type_action: TypeAction, share: schemas.ShareInput,
                            db: Session = Depends(get_db)):
    response_data = api.get_data_for_symbol(symbol)
    if response_data['status']['rCode'] == 400:
        error = 'Symbol not found'
        raise HTTPException(status_code=404, detail=error)
    data = response_data['data']

    company = schemas.CompanyInput(name=data['companyName'], symbol=data['symbol'])
    db_company = crud.get_company_or_create(db, company)

    symbol_currency, price_unit = split_symbol_and_number(data['primaryData']['lastSalePrice'])
    share_quantity = share.quantity

    if type_action == TypeAction.sell:
        share_quantity = share_quantity * -1

    share_total = schemas.ShareTotal(quantity=share_quantity,
                                     price_unit=price_unit,
                                     symbol_currency=symbol_currency)
    db_share = crud.create_share(db, share_total, db_company.id)

    # todo: Personalizar la respuesta
    return db_share
