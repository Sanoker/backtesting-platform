from pydantic import BaseModel


class FilterConfig(
    BaseModel
):

    min_market_cap: float | None = None

    max_market_cap: float | None = None

    min_roce: float | None = None

    positive_pat: bool = False


class RankingMetric(
    BaseModel
):

    name: str

    ascending: bool


class BacktestRequest(
    BaseModel
):

    start_date: str

    end_date: str

    portfolio_size: int

    rebalance: str

    capital: float

    filters: FilterConfig

    rankings: list[
        RankingMetric
    ]