import pandas as pd


def generate_rebalance_dates(
    start_date,
    end_date,
    frequency
):

    freq_map = {
        "monthly": "M",
        "quarterly": "Q",
        "yearly": "Y"
    }

    return pd.date_range(
        start=start_date,
        end=end_date,
        freq=freq_map[frequency]
    )