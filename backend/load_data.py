from app.database import SessionLocal
from app.database import Base
from app.database import engine

from app.services.nifty100 import NIFTY_STOCKS

from app.services.data_fetcher import (
    get_stock_data,
    save_stock,
    save_prices,
    save_fundamentals
)

from sqlalchemy import inspect
from sqlalchemy import text


def ensure_database_schema():
    Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)
    dialect = engine.dialect

    with engine.begin() as connection:
        for table in Base.metadata.sorted_tables:
            existing_columns = {
                column["name"]
                for column in inspector.get_columns(table.name)
            }

            for column in table.columns:
                if column.name in existing_columns or column.primary_key:
                    continue

                column_type = column.type.compile(dialect=dialect)
                connection.execute(
                    text(
                        f"ALTER TABLE {table.name} "
                        f"ADD COLUMN {column.name} {column_type}"
                    )
                )


ensure_database_schema()

db = SessionLocal()

try:
    for symbol in NIFTY_STOCKS:

        print(f"Fetching {symbol}")

        data = get_stock_data(symbol)

        if not data:
            continue

        stock = save_stock(
            db,
            symbol,
            data["info"]
        )

        save_prices(
            db,
            stock.id,
            data["history"]
        )

        save_fundamentals(
            db,
            stock.id,
            data["info"]
        )
finally:
    db.close()

print("Done")
