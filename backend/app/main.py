from fastapi import FastAPI

app = FastAPI(
    title="Equity Backtesting API",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Backtesting Platform API Running"
    }