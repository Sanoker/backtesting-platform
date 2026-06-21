import yfinance as yf
from app.models.fundamentals import Fundamental
from app.models.stock import Stock
from app.models.stock_price import StockPrice


def get_stock_data(symbol):
    try:
        ticker = yf.Ticker(symbol)

        info = ticker.info

        history = ticker.history(
            start="2018-01-01",
            end="2025-01-01"
        )

        return {
            "info": info,
            "history": history
        }

    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None


def clean_number(value):
    if value != value:
        return None

    return value


def save_stock(db, symbol, info):
    stock = db.query(Stock).filter(Stock.symbol == symbol).first()

    if stock:
        stock.company_name = info.get("longName")
        stock.sector = info.get("sector")
    else:
        stock = Stock(
            symbol=symbol,
            company_name=info.get("longName"),
            sector=info.get("sector")
        )

        db.add(stock)

    db.commit()
    db.refresh(stock)

    return stock

def save_prices(db, stock_id, history):
    db.query(StockPrice).filter(
        StockPrice.stock_id == stock_id
    ).delete()

    for date, row in history.iterrows():

        price = StockPrice(
            stock_id=stock_id,
            trade_date=date.date(),
            open_price=clean_number(row["Open"]),
            high_price=clean_number(row["High"]),
            low_price=clean_number(row["Low"]),
            close_price=clean_number(row["Close"]),
            volume=int(row["Volume"]) if clean_number(row["Volume"]) is not None else None
        )

        db.add(price)

    db.commit()


def save_fundamentals(db, stock_id, info):
    db.query(Fundamental).filter(
        Fundamental.stock_id == stock_id
    ).delete()

    fundamental = Fundamental(
        stock_id=stock_id,

        market_cap=info.get(
            "marketCap"
        ),

        roe=info.get(
            "returnOnEquity"
        ),

        pe_ratio=info.get(
            "trailingPE"
        ),

        pb_ratio=info.get(
            "priceToBook"
        ),

        debt_to_equity=info.get(
            "debtToEquity"
        )
    )

    db.add(fundamental)

    db.commit()
