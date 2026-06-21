from fastapi import FastAPI

from app.database import Base
from app.database import engine

from app.models.stock import Stock

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Equity Backtesting API"
)

@app.get("/")
def home():
    return {
        "message": "API Running"
    }