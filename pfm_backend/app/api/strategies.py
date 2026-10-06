from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.analytics import _month_range, _sum_for_type
from app.api.deps import get_current_user
from app.database import get_db
from app.models import User
from app.schemas import StrategyResponse
from app.services.strategy_engine import generate_strategy

router = APIRouter(prefix="/strategies", tags=["strategies"])


@router.get("/recommendation", response_model=StrategyResponse)
def get_recommendation(
    year: int | None = Query(None, ge=2000),
    month: int | None = Query(None, ge=1, le=12),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    today = date.today()
    year = year or today.year
    month = month or today.month
    start, end = _month_range(year, month)

    total_income = _sum_for_type(db, current_user.id, "income", start, end)
    total_expenses = _sum_for_type(db, current_user.id, "expense", start, end)
    return generate_strategy(total_income, total_expenses)