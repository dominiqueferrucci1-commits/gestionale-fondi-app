from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models import Category, Transaction, User
from app.schemas import CategorySummaryResponse, MonthlySummaryResponse

router = APIRouter(prefix="/analytics", tags=["analytics"])


def _month_range(year: int, month: int) -> tuple[date, date]:
    if month == 12:
        return date(year, 12, 1), date(year + 1, 1, 1)
    return date(year, month, 1), date(year, month + 1, 1)


def _sum_for_type(
    db: Session, user_id: int, category_type: str, start: date, end: date
) -> float:
    total = (
        db.query(func.coalesce(func.sum(Transaction.amount_cents), 0))
        .join(Category, Transaction.category_id == Category.id)
        .filter(
            Transaction.user_id == user_id,
            Category.type == category_type,
            Transaction.date >= start,
            Transaction.date < end,
        )
        .scalar()
    )
    return round(total / 100, 2)


@router.get("/monthly", response_model=MonthlySummaryResponse)
def monthly_summary(
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
    net_balance = round(total_income - total_expenses, 2)
    savings_rate = round(net_balance / total_income * 100, 2) if total_income else 0.0

    return MonthlySummaryResponse(
        year=year,
        month=month,
        total_income=total_income,
        total_expenses=total_expenses,
        net_balance=net_balance,
        savings_rate=savings_rate,
    )


@router.get("/by-category", response_model=list[CategorySummaryResponse])
def expenses_by_category(
    year: int | None = Query(None, ge=2000),
    month: int | None = Query(None, ge=1, le=12),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    today = date.today()
    year = year or today.year
    month = month or today.month
    start, end = _month_range(year, month)

    rows = (
        db.query(Category.name, func.sum(Transaction.amount_cents).label("total_cents"))
        .join(Transaction, Transaction.category_id == Category.id)
        .filter(
            Transaction.user_id == current_user.id,
            Category.type == "expense",
            Transaction.date >= start,
            Transaction.date < end,
        )
        .group_by(Category.name)
        .order_by(func.sum(Transaction.amount_cents).desc())
        .all()
    )
    return [
        CategorySummaryResponse(category_name=name, total=round(cents / 100, 2))
        for name, cents in rows
    ]