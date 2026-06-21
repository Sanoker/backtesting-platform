from fastapi import FastAPI

from app.database import Base
from app.database import engine
from app.routers.stocks import router
from app.models.stock import Stock
from app.models.stock_price import StockPrice
from app.models.fundamentals import Fundamental

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "API Running"
    }

app.include_router(
    router,
    prefix="/stocks",
    tags=["Stocks"]
)

from app.routers.backtest import (
    router as backtest_router
)

app.include_router(
    backtest_router,
    prefix="/backtest",
    tags=["Backtest"]
)