import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db import Base
from main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_status(test_db):
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_create_share(test_db):
    test_symbol = 'AAPL'
    test_type_action = 'buy'
    response = client.post(f"/share/{test_symbol}/{test_type_action}",
                           json={"quantity": 3})
    assert response.status_code == 200


def test_create_share_not_found(test_db):
    test_symbol = 'AAPL2'
    test_type_action = 'buy'
    response = client.post(f"/share/{test_symbol}/{test_type_action}",
                           json={"quantity": 3})
    assert response.status_code == 404
    assert response.json() == {'detail': 'Symbol not found'}


def test_create_share_sell_error(test_db):
    test_symbol = 'GOOG'

    # First, buy shares
    test_action_buy = 'buy'
    client.post(f"/share/{test_symbol}/{test_action_buy}",
                json={"quantity": 3})

    test_action_sell = 'sell'
    response = client.post(f"/share/{test_symbol}/{test_action_sell}",
                           json={"quantity": 4})
    assert response.status_code == 422
    assert response.json() == {'detail': 'It does not contain enough shares to sell'}


def test_create_shares(test_db):
    response = client.get("/shares")
    assert response.status_code == 200


def test_prices_history_by_symbol(test_db):
    test_symbol = 'AAPL'
    response = client.get(f"/prices_history/{test_symbol}")
    assert response.status_code == 200
