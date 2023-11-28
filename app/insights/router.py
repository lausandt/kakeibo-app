from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.jwt import oauth2_scheme
from app.budget import crud as budget_crud
from app.budget.schema import Budget, BudgetCreate
from app.core.dependecies import (
    get_current_active_super_user,
    get_current_period,
    get_db,
)
from app.entry import crud as entry_crud
from app.entry.schema import Entry
from app.models.models import Period, User
from app.period import crud as period_crud
from app.period import schema
from app.user import crud as user_crud

from . import crud

router = APIRouter(
    prefix="/insights",
    tags=["Insights"],
    dependencies=[Depends(oauth2_scheme)],
)


@router.post(
    "/load_fixed_entries_for_period", status_code=201, response_model=schema.Period
)
async def load_fixeds_for_period(
    period: Period = Depends(get_current_period),
    db: Session = Depends(get_db),
    super_user: User = Depends(get_current_active_super_user),
):
    per = period_crud.period.load_fixed_for_period(
        db=db, period=period, owner_id=int(super_user.id)
    )
    return per


@router.get("/get_entries_for_period", status_code=200, response_model=list[Entry])
async def get_entries_for_period(
    period=Depends(get_current_period), db=Depends(get_db)
):
    return entry_crud.entry.get_entries_by_period(db=db, period=period)


@router.get(
    "/total_expenses_current_period/",
    response_model=dict[str, int | float],
    status_code=200,
)
async def total_expenses_current_period(
    period: Period = Depends(get_current_period),
    db: Session = Depends(get_db),
    super_user: User = Depends(get_current_active_super_user),
):
    total = crud.get_total_monthly_expenses(db=db, period_nr=int(period.nr))
    return {"the total monthly expenses are": total}


@router.get(
    "/total_monthly_expenses/{period}",
    response_model=dict[str, float | int],
    status_code=200,
)
async def total_monthly_expenses(
    period_nr: int,
    db: Session = Depends(get_db),
    super_user: User = Depends(get_current_active_super_user),
):

    exp = crud.get_total_monthly_expenses(db=db, period_nr=period_nr)
    return {"this months total expenses are": exp}


@router.get(
    "/total_monthly_regular_expenses",
    response_model=dict[str, float | int],
    status_code=200,
)
async def total_monthly_regular_expenses(
    period: Period = Depends(get_current_period),
    db: Session = Depends(get_db),
    super_user: User = Depends(get_current_active_super_user),
):
    exp = crud.get_total_monthly_regular_expenses(db=db, period_nr=period.nr)
    return {"this months total regular expenses are": exp}


@router.get(
    "/total_monthly_fixeds_expenses",
    response_model=dict[str, float | int],
    status_code=200,
)
async def total_monthly_fixed_expenses(
    period: Period = Depends(get_current_period),
    db: Session = Depends(get_db),
    super_user: User = Depends(get_current_active_super_user),
):
    exp = crud.get_total_monthly_expenses(
        db=db, period_nr=int(period.nr)
    ) - crud.get_total_monthly_regular_expenses(db=db, period_nr=period.nr)
    return {"this months total fixed expenses are": exp}


@router.get("/monthly_expenses_user/{id}")
async def monthly_expenses_user(
    user_id: int,
    period: Period = Depends(get_current_period),
    db: Session = Depends(get_db),
    super_user: User = Depends(get_current_active_super_user),
):
    user = user_crud.user.get_user_by_id(db=db, id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.monthly_expenses_user(user=user, period_nr=int(period.nr))


@router.get("/monthly_expenses_user_by_mail/{email}")
async def monthly_expenses_user_email(
    email: str,
    period: Period = Depends(get_current_period),
    db: Session = Depends(get_db),
    super_user: User = Depends(get_current_active_super_user),
):
    user = user_crud.user.get_user_by_email(db=db, email=email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.monthly_expenses_user(user=user, period_nr=int(period.nr))


@router.get('/period_expenses_per_supplier/{supplier}', response_model=dict[str, float], status_code=200)
async def expenses_per_supplier(
    supplier: str,
    period: Period = Depends(get_current_period),
    db: Session = Depends(get_db),
    super_user = Depends(get_current_active_super_user)
):
    value = crud.get_total_monthly_expenses_with_supplier(db=db, supplier=supplier, period_nr=int(period.nr))
    if value is None:
        raise HTTPException(
            status_code=400,
            detail='supplier was not found'
        )
    return {f'for this period, the amount spent with {supplier} is':value}


@router.get('/period_expenses_per_subject/{subject}', response_model=dict[str, float], status_code=200)
async def expenses_per_subject(
    subject: str,
    period: Period = Depends(get_current_period),
    db: Session = Depends(get_db),
    super_user = Depends(get_current_active_super_user)
):
    value = crud.get_total_monthly_expenses_per_subject(db=db, subject=subject, period_nr=int(period.nr))
    if value is None:
        raise HTTPException(
            status_code=400,
            detail='supplier was not found'
        )
    return {f'for this period, the amount spent on {subject} is':value}



@router.post("/budget", status_code=201, response_model=Budget)
async def add_budget(
    budget: BudgetCreate,
    db: Session = Depends(get_db),
    super_user: User = Depends(get_current_active_super_user),
):
    """add the periodic budget to the kakeibo"""
    return budget_crud.budget.add_budget(
        db=db, budget=budget, user_id=int(super_user.id)
    )


@router.get(
    "/budget_for_current_period", status_code=200, response_model=dict[str, int | float]
)
async def show_budget(
    period: Period = Depends(get_current_period),
    db: Session = Depends(get_db),
    super_user: User = Depends(get_current_active_super_user),
):
    value = budget_crud.budget.show_budget_for_period(db=db, period_id=int(period.nr))
    if value == 0:
        raise HTTPException(
            status_code=404, detail="There is no budget for this period"
        )
    return {"the remaining budget for this month is": value}
