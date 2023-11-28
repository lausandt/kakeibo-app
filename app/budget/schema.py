from datetime import date

from pydantic import BaseModel, Field


class BudgetBase(BaseModel):
    period_id: int = Field(gt=0, lt=13)
    amount: float | int = 0


class BudgetCreate(BudgetBase):
    entry_date: date = date.today()


class Budget(BudgetCreate):
    id: int
    owner_id: int

    class ConfigDict:
        from_attributes = True
