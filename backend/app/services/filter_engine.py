import pandas as pd


def apply_filters(df, filters):

    if filters.get("min_market_cap"):
        df = df[
            df["market_cap"] >=
            filters["min_market_cap"]
        ]

    if filters.get("max_market_cap"):
        df = df[
            df["market_cap"] <=
            filters["max_market_cap"]
        ]

    if filters.get("min_roce"):
        df = df[
            df["roce"] >=
            filters["min_roce"]
        ]

    if filters.get("positive_pat"):

        df = df[
            df["net_profit"] > 0
        ]

    return df