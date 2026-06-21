import pandas as pd
from sqlalchemy import text

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

def load_prices(db):

    query = text("""

        SELECT

        stock_id,
        trade_date,
        close_price

        FROM stock_prices

    """)

    result = db.execute(query)

    rows = result.fetchall()

    return pd.DataFrame(
        rows,
        columns=[
            "stock_id",
            "trade_date",
            "close_price"
        ]
    )

def equal_weight(
    selected
):

    weight = (
        1 /
        len(selected)
    )

    return {
        stock: weight
        for stock in selected
    }

def market_cap_weight(df):

    total = df[
        "market_cap"
    ].sum()

    weights = {}

    for _, row in df.iterrows():

        weights[
            row["stock_id"]
        ] = (
            row["market_cap"]
            /
            total
        )

    return weights

def metric_weight(df):

    total = df[
        "roce"
    ].sum()

    weights = {}

    for _, row in df.iterrows():

        weights[
            row["stock_id"]
        ] = (
            row["roce"]
            /
            total
        )

    return weights

def calculate_period_return(
    prices,
    stock_id,
    start_date,
    end_date
):

    stock_prices = prices[
        prices["stock_id"]
        ==
        stock_id
    ]

    start_row = stock_prices[
        stock_prices["trade_date"]
        >= start_date
    ].head(1)

    end_row = stock_prices[
        stock_prices["trade_date"]
        <= end_date
    ].tail(1)

    if (
        start_row.empty
        or
        end_row.empty
    ):
        return 0

    start_price = (
        start_row[
            "close_price"
        ]
        .iloc[0]
    )

    end_price = (
        end_row[
            "close_price"
        ]
        .iloc[0]
    )

    return (
        end_price
        -
        start_price
    ) / start_price

def portfolio_return(
    weights,
    prices,
    start_date,
    end_date
):

    total_return = 0

    for stock_id, weight in weights.items():

        stock_return = (
            calculate_period_return(
                prices,
                stock_id,
                start_date,
                end_date
            )
        )

        total_return += (
            stock_return
            *
            weight
        )

    return total_return

def run_backtest(
    fundamentals,
    prices,
    start_date,
    end_date,
    rebalance,
    portfolio_size,
    position_type,
    filters,
    rankings,
    capital
):

rebalance_dates = (
    generate_rebalance_dates(
        start_date,
        end_date,
        rebalance
    )
)

equity = capital

equity_curve = []

portfolio_logs = []

for i in range(
    len(rebalance_dates)-1
):
    
current_date = (
    rebalance_dates[i]
)

next_date = (
    rebalance_dates[i+1]
)

current_fundamentals = (
    fundamentals[
        fundamentals[
            "report_date"
        ]
        <= current_date
    ]
)

filtered = apply_filters(
    current_fundamentals,
    filters
)

ranked = composite_rank(
    filtered,
    rankings
)

selected = ranked.head(
    portfolio_size
)

if (
    position_type
    ==
    "equal"
):

    weights = (
        equal_weight(
            selected[
                "stock_id"
            ].tolist()
        )
    )

elif (
    position_type
    ==
    "market_cap"
):

    weights = (
        market_cap_weight(
            selected
        )
    )

else:

    weights = (
        metric_weight(
            selected
        )
    )

period_return = (
    portfolio_return(
        weights,
        prices,
        current_date,
        next_date
    )
)

equity = (
    equity *
    (
        1 +
        period_return
    )
)

equity_curve.append({
    "date":
    next_date.strftime(
        "%Y-%m-%d"
    ),
    "equity":
    round(equity,2)
})

portfolio_logs.append({
    "rebalance_date":
    current_date.strftime(
        "%Y-%m-%d"
    ),

    "stocks":
    selected[
        "stock_id"
    ].tolist(),

    "return":
    round(
        period_return,
        4
    )
})

return {

    "final_value":
    equity,

    "equity_curve":
    equity_curve,

    "portfolio_logs":
    portfolio_logs
}

