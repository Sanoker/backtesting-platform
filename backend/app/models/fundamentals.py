from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import BigInteger
from sqlalchemy import Date
from sqlalchemy import ForeignKey

from app.database import Base


class Fundamental(Base):
    __tablename__ = "fundamentals"

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

    report_date = Column(Date)

    market_cap = Column(BigInteger)

    roe = Column(Float)

    roce = Column(Float)

    pe_ratio = Column(Float)

    net_profit = Column(Float)