from fastapi import FastAPI

app = FastAPI()


@app.get("/status")
async def root():
    return {"status": "ready"}


@app.get("/share/{symbol}")
async def read_user_item(symbol):
    item = {"symbol": symbol}
    return item
