from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from enum import Enum

import crud
import schemas
from api import api
from db import SessionLocal, engine, Base
from schemas import ActionWithShareResponseModel, TypeAction
from utils import split_symbol_and_number, get_change, average

Base.metadata.create_all(bind=engine)

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


@app.post("/share/{symbol}/{type_action}",
          response_model=ActionWithShareResponseModel)
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

    # todo: hacer la validacion de no vender mas acciones si no tiene acciones compradas.

    share_total = schemas.ShareTotal(quantity=share.quantity,
                                     price_unit=price_unit,
                                     symbol_currency=symbol_currency,
                                     type_action=type_action)

    crud.create_share(db, share_total, db_company.id)

    result = {
        'data': {
            'quantity': share.quantity,
            'price_unit': f'{symbol_currency}{price_unit}',
            'type_action': type_action,
            'company': db_company.name,
            'symbol_company': symbol,
        },
        'message': 'Successful operation'
    }
    return result


@app.get("/shares")
async def list_share(db: Session = Depends(get_db)):
    shares = crud.get_share_all(db)

    total_share_company = {}
    for share in shares:
        symbol = share.company.symbol
        if symbol not in total_share_company:
            total_share_company[symbol] = {
                'company_name': share.company.name,
                'total_share': 0,
                'quantity_share': 0,
                'prices': []
            }

        multiplier = -1 if share.type_action == TypeAction.sell else 1

        total_share_company[symbol]['total_share'] += share.quantity * share.price_unit * multiplier
        total_share_company[symbol]['quantity_share'] += share.quantity * multiplier
        total_share_company[symbol]['prices'].append(share.price_unit)

    symbols = total_share_company.keys()

    for symbol in symbols:
        quantity_total = total_share_company[symbol]['quantity_share']
        symbol_currency, price_share_now = split_symbol_and_number(
            api.get_data_for_symbol(symbol)['data']['primaryData']['lastSalePrice'])
        total_share_now = quantity_total * float(price_share_now)
        total_share_company[symbol]['total_share_now'] = total_share_now

        total_share_company[symbol]['profit_or_loss_percentage'] = get_change(total_share_now,
                                                                              total_share_company[symbol][
                                                                                  'total_share'])

        total_share_company[symbol]['symbol_currency'] = symbol_currency

        # Lowest Price , Highest Price, Average Price
        price_sort = total_share_company[symbol].pop('prices')
        price_sort.sort()

        total_share_company[symbol].update({
            'lowest_price': price_sort[0],
            'highest_price': price_sort[-1],
            'average_price': average(price_sort)
        })

    # Round values
    values_round = ['total_share', 'total_share_now', 'profit_or_loss_percentage', 'average_price']
    round_decimal = 2
    for symbol in symbols:
        for value in values_round:
            total_share_company[symbol][value] = round(total_share_company[symbol][value], round_decimal)

    return total_share_company


# Todo: agregar scheduler
@app.get("/prices_history/{symbol}")
async def prices_history(symbol: str, db: Session = Depends(get_db)):
    print(symbol)
    return symbol
