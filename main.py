from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List

import crud
import schemas
from api import api
from db import SessionLocal, engine, Base, SessionMarkerFastAPI
from utils import split_symbol_and_number, get_change, average
from fastapi_utils.tasks import repeat_every

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/status")
async def status():
    return {"status": "ready"}


@app.post("/share/{symbol}/{type_action}",
          response_model=schemas.ActionWithShareResponseModel)
async def create_share(symbol: str, type_action: schemas.TypeAction, share: schemas.ShareInput,
                            db: Session = Depends(get_db)):
    # Extraction of information from the api
    response_data = api.get_data_for_symbol(symbol)

    # Validate if the symbol exists
    if response_data['status']['rCode'] == 400:
        error = 'Symbol not found'
        raise HTTPException(status_code=404, detail=error)

    data = response_data['data']

    # Create Company if not exist
    company = schemas.CompanyInput(name=data['companyName'], symbol=data['symbol'])
    db_company = crud.get_company_or_create(db, company)

    # Create Share
    symbol_currency, price_unit = split_symbol_and_number(data['primaryData']['lastSalePrice'])
    share_total = schemas.ShareTotal(quantity=share.quantity,
                                     price_unit=price_unit,
                                     symbol_currency=symbol_currency,
                                     type_action=type_action)
    share_create = crud.create_share(db, share_total, db_company.id)

    # Validation sell
    if share_create is None:
        error = 'It does not contain enough shares to sell'
        raise HTTPException(status_code=422, detail=error)
    result = {
        'quantity': share.quantity,
        'price_unit': f'{symbol_currency}{price_unit}',
        'type_action': type_action,
        'company': db_company.name,
        'symbol_company': symbol,
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

        multiplier = -1 if share.type_action == schemas.TypeAction.sell else 1

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


# Scheduler with interval 1 hour
@app.on_event("startup")
@repeat_every(seconds=60 * 60)
def history_prices_for_symbol() -> None:
    try:
        with SessionMarkerFastAPI.context_session() as db:
            companies = crud.get_company_all(db)
            for company in companies:
                response_data = api.get_data_for_symbol(company.symbol)

                data = response_data['data']
                symbol_currency, price_unit = split_symbol_and_number(data['primaryData']['lastSalePrice'])
                price_history_total = schemas.PriceHistoryTotal(price_unit=price_unit,
                                                                symbol_currency=symbol_currency)
                crud.create_price_history(db, price_history_total, company.id)

    except Exception as err:
        print(err)


@app.get("/prices_history/{symbol}",
         response_model=List[schemas.PricesHistoryBySymbolResponseModel])
async def prices_history_by_symbol(symbol: str, db: Session = Depends(get_db)):
    prices_history = crud.get_price_history_by_symbol(db, symbol)

    result = []
    for price_history in prices_history:
        result.append({
            'price_unit': f'{price_history.symbol_currency}{price_history.price_unit}',
            'create_date': price_history.create_date
        })
    return result
