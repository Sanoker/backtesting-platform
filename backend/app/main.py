from fastapi import FastAPI

from app.database import Base
from app.database import engine

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