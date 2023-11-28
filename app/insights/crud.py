from sqlalchemy.orm import Session

from app.models.models import Entry
from app.user.schema import User


def get_total_monthly_expenses(db: Session, period_nr: int) -> float | int:
    entries = db.query(Entry).filter(Entry.period_id == period_nr).all()
    return sum([float(e.amount) for e in entries])


def get_total_monthly_regular_expenses(db: Session, period_nr) -> float:
    entries = db.query(Entry).filter(Entry.period_id == period_nr).all()
    return sum([float(e.amount) for e in entries if not e.interval])


def monthly_expenses_user(user: User, period_nr: int) -> dict[str, object]:
    period_entries = list(filter(lambda x: x.period_id == period_nr, user.entries))
    res = {
        "user": user.name,
        "amount": round(sum([e.amount for e in period_entries]), 2),
    }
    return res


def get_total_monthly_expenses_with_supplier(db:Session, supplier:str, period_nr:int) -> float:
    expenses = db.query(Entry).filter(Entry.period_id == period_nr, Entry.supplier == supplier).all()
    return sum([e.amount for e in expenses])

def get_total_monthly_expenses_per_subject(db: Session, subject: str, period_nr: int) -> float:
    expenses = db.query(Entry).filter(Entry.period_id == period_nr, Entry.title == subject).all()
    return sum([e.amount for e in expenses])
