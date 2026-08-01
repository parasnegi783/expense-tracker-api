from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class ExpenseCreate(BaseModel):
    title: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)
    category: str = Field(..., min_length=1)
    date: date


class Expense(ExpenseCreate):
    id: int


class CategoryTotal(BaseModel):
    category: str
    total: float


class TotalResponse(BaseModel):
    total: float
    by_category: list[CategoryTotal]
