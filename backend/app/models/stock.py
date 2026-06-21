from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.database import Base


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    symbol = Column(
        String(20),
        unique=True,
        nullable=False
    )

    company_name = Column(
        String(255)
    )

    sector = Column(
        String(100)
    )