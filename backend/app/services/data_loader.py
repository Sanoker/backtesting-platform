import pandas as pd

from sqlalchemy import text

def load_fundamentals(db):

    query = text("""

        SELECT

        stock_id,

        market_cap,

        roe,

        roce,

        pe_ratio,

        net_profit

        FROM fundamentals

    """)

    result = db.execute(query)

    rows = result.fetchall()

    return pd.DataFrame(rows)