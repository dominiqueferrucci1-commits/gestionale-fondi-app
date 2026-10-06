import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CategoryType(str, Enum):
    income = "income"
    expense = "expense"


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    is_active: bool


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1)
    type: CategoryType


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: CategoryType


class TransactionCreate(BaseModel):
    amount: float = Field(gt=0)
    category_id: int
    date: datetime.date | None = None
    description: str | None = None


class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    amount: float
    date: datetime.date
    description: str | None
    category_id: int


class MonthlySummaryResponse(BaseModel):
    year: int
    month: int
    total_income: float
    total_expenses: float
    net_balance: float
    savings_rate: float


class CategorySummaryResponse(BaseModel):
    category_name: str
    total: float


class ActionPlanItem(BaseModel):
    action_name: str
    amount: float
    description: str


class StrategyResponse(BaseModel):
    net_balance: float
    savings_rate: float
    status: str
    recommendations: list[ActionPlanItem]


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str