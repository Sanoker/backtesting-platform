from sqlalchemy import Column, Integer, BigInteger
from sqlalchemy import Float, Date, ForeignKey

from app.database import Base


class StockPrice(Base):
    __tablename__ = "stock_prices"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    stock_id = Column(
        Integer,
        ForeignKey("stocks.id"),
        nullable=False
    )

    trade_date = Column(
        Date,
        nullable=False
    )

    open_price = Column(Float)

    high_price = Column(Float)

    low_price = Column(Float)

    close_price = Column(Float)

    volume = Column(BigInteger)