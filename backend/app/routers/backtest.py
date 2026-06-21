from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.schemas.backtest import BacktestRequest

from app.services.data_loader import (
    load_fundamentals,
    load_prices
)

from app.services.backtest_engine import (
    run_backtest
)

router = APIRouter()


@router.post("/run")
def run_strategy(
    request: BacktestRequest,
    db: Session = Depends(get_db)
):

    fundamentals = load_fundamentals(db)

    prices = load_prices(db)

    result = run_backtest(
        fundamentals=fundamentals,
        prices=prices,

        start_date=request.start_date,
        end_date=request.end_date,

        rebalance=request.rebalance,

        portfolio_size=request.portfolio_size,

        position_type="equal",

        filters=request.filters.model_dump(),

        rankings=[
            ranking.model_dump()
            for ranking in request.rankings
        ],

        capital=request.capital
    )

    return result