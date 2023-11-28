from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.jwt import oauth2_scheme
from app.core.dependecies import get_current_period, get_current_user, get_db
from app.entry.schema import Entry, EntryCreate
from app.models import models

from . import crud, schema

router = APIRouter(
    prefix="/users", tags=["Users"], dependencies=[Depends(oauth2_scheme)]
)


@router.get("/get_users/", response_model=list[dict[str, Any]], status_code=200)
async def read_all_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Get all the users in the system"""
    users = crud.user.get_users(db=db, skip=skip, limit=limit)
    return users


@router.get("/{email}/get_user/", response_model=schema.User, status_code=200)
async def get_user_by_name(email: str, db: Session = Depends(get_db)):
    return crud.user.get_user_by_email(db=db, email=email)


@router.post("/me/new_entry/", response_model=Entry, status_code=201)
async def create_entry_for_user(
    entry: EntryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    period: models.Period = Depends(get_current_period),
):
    """Create an entry for the current logged in user"""
    if not current_user.active:
        raise HTTPException(
            status_code=400, detail="only active users can make entries in the kakeibo"
        )
    entry = crud.user.create_entry_for_user(
        db=db, entry=entry, user_id=int(current_user.id), period_id=int(period.nr)
    )
    return entry
