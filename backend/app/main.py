from fastapi import FastAPI

from app.database import Base
from app.database import engine

from app.models.stock import Stock
from app.models.stock_price import StockPrice
from app.models.fundamentals import Fundamental

from app.routers.backtest import router as backtest_router
from app.routers.stocks import router as stock_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Equity Backtesting API",
    version="1.0.0"
)

app.include_router(
    backtest_router,
    prefix="/backtest",
    tags=["Backtest"]
)

app.include_router(
    stock_router,
    prefix="/stocks",
    tags=["Stocks"]
)


@app.get("/")
def home():
    return {
        "message": "Backtesting Platform API Running"
    }