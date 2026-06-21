from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.schemas.backtest import (
    BacktestRequest
)

router = APIRouter()


@router.post("/test")
def test_strategy(
    request: BacktestRequest,
    db: Session = Depends(
        get_db
    )
):

    return {
        "message":
        "Strategy received",
        "portfolio_size":
        request.portfolio_size
    }