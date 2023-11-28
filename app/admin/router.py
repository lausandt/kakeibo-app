from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.jwt import oauth2_scheme
from app.core.dependecies import get_current_active_super_user, get_db
from app.entry import crud as entry_crud
from app.entry.schema import Entry, EntryCreate, FixedEntry, FixedEntryCreate
from app.models.models import User
from app.period import crud as period_crud
from app.period.schema import Period, PeriodCreate
from app.user import crud as user_crud
from app.user import schema

router = APIRouter(
    prefix="/admin", tags=["Admin"], dependencies=[Depends(oauth2_scheme)]
)


@router.post(
    "/user/signup",
    response_model=schema.User,
    status_code=201,
)
async def user_signup(
    user_in: schema.UserCreate,
    db: Session = Depends(get_db),
    super_user: User = Depends(get_current_active_super_user),
) -> Any:
    """
    Create new user
    """
    user = db.query(User).filter(User.email == user_in.email).first()  # type: ignore
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user = user_crud.user.create_user(db=db, user=user_in)
    return user


@router.patch(
    "/user/{id}/set_user_active_level", response_model=schema.User, status_code=201
)
async def set_user_active_level(
    id: int,
    db: Session = Depends(get_db),
    superuser: User = Depends(get_current_active_super_user),
):
    """function to toggle if the user is active"""
    user = user_crud.user.set_active_level(db=db, user_id=id)
    if not user:
        raise HTTPException(
            status_code=400,
            detail=f"There is no user with this {id} in the system",
        )
    return user


@router.patch("/users/{id}/set_super_user", response_model=schema.User, status_code=200)
async def set_super_user(
    id: int,
    db: Session = Depends(get_db),
    superuser: User = Depends(get_current_active_super_user),
):
    user = user_crud.user.set_super_user(db=db, user_id=id)  # type: ignore
    if not user:
        raise HTTPException(
            status_code=400,
            detail=f"There is no user with this id {id} in the system",
        )
    return user


@router.post("/user/{id}/create_entry_for_user", response_model=Entry, status_code=201)
async def create_entry_for_user(
    entry: EntryCreate,
    user_id: int,
    db: Session = Depends(get_db),
    super_user: User = Depends(get_current_active_super_user)
    # period: models.Period = Depends(get_current_period),
):
    """admin function creates an entry for a user does not check if user is active"""

    return user_crud.user.create_entry_for_user(
        db=db,
        entry=entry,
        user_id=user_id,
        period_id=11,  # int(period.nr)   type: ignore
    )


@router.post(
    "/fixed_entries/create_fixed_entry",
    response_model=FixedEntryCreate,
    status_code=201,
)
async def create_fixed_entry(
    entry_in: FixedEntryCreate,
    super_user: User = Depends(get_current_active_super_user),
):
    return entry_crud.entry.create_fixed_entry_json(entry=entry_in)  # type: ignore


@router.post("/period/create_periods", response_model=Period, status_code=201)
async def create_period(
    period: PeriodCreate,
    db: Session = Depends(get_db),
    super_user: User = Depends(get_current_active_super_user),
):
    return period_crud.period.create_period(db=db, period=period)


@router.put("/period/update_period", response_model=Period, status_code=201)
async def update_period(
    period_in: PeriodCreate,
    db: Session = Depends(get_db),
    super_user: User = Depends(get_current_active_super_user),
):
    period = period_crud.period.update_period(db=db, period=period_in)
    if period is None:
        raise HTTPException(status_code=400, detail="period not found")
    return period


@router.delete(
    "/entries/{id}/delete_entry", status_code=200, response_model=schema.Entry
)
async def remove(
    id: int,
    db: Session = Depends(get_db),
    super_user: User = Depends(get_current_active_super_user),
):
    entry = entry_crud.entry.remove(db=db, entry_id=id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry


@router.delete(
    "/fixed_entry/{id}/remove_fixed_entry_from_database", response_model=FixedEntry
)
async def remove_fixed_entry(
    id: int,
    db: Session = Depends(get_db),
    super_user: User = Depends(get_current_active_super_user),
):

    fixed = entry_crud.entry.remove_fixed(db=db, id=id)
    if not fixed:
        raise HTTPException(
            status_code=400,
            detail=f"There is no fixed entry with id: {id}, in the system",
        )
    return fixed


@router.delete("/period/{nr}/delete_period", response_model=Period, status_code=200)
async def delete_period(
    nr: int,
    db: Session = Depends(get_db),
    super_user: User = Depends(get_current_active_super_user),
):
    period = period_crud.period.delete_period(db=db, nr=nr)
    if period is None:
        raise HTTPException(status_code=400, detail="period not found")
    return period


@router.delete("/user/{id}/delete_user/", response_model=schema.User, status_code=200)
async def delete_user(
    id: int,
    db: Session = Depends(get_db),
    super_user: User = Depends(get_current_active_super_user),
):
    user = user_crud.user.remove(db=db, user_id=id)
    if not user:
        raise HTTPException(
            status_code=400,
            detail=f"There is no user with this {id} in the system",
        )
    return user
