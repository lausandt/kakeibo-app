from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.insights.crud import get_total_monthly_expenses
from app.models.models import Budget

from .schema import BudgetCreate


@dataclass
class BudgetCRUD:

    model: type[Budget]

    def add_budget(self, db: Session, budget: BudgetCreate, user_id: int) -> Budget:
        db_budget = Budget(**budget.model_dump(), owner_id=user_id)
        db.add(db_budget)
        db.commit()
        db.refresh(db_budget)
        return db_budget

    def show_budget_for_period(self, db: Session, period_id: int) -> int | float:
        budget = db.query(self.model).filter(self.model.period_id == period_id).first()
        if budget is None:
            return 0
        remainder = budget.amount - get_total_monthly_expenses(
            db=db, period_nr=period_id
        )
        return round(remainder, 2)


budget = BudgetCRUD(model=Budget)
