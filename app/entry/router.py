from typing import Any, Sequence

import jsonlines
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.jwt import oauth2_scheme
from app.core.dependecies import get_current_period, get_current_user, get_db
from app.models.models import Period, User

from . import crud, schema

router = APIRouter(
    prefix="/entries",
    tags=["Entries"],
    dependencies=[Depends(oauth2_scheme)],
)


@router.get("/show_entries_me", status_code=200, response_model=Sequence[schema.Entry])
async def fetch_all_entries_me(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return [e for e in crud.entry.get_entries(db=db) if e.owner_id == user.id]


@router.get("/get_entry/{id}", status_code=200, response_model=schema.Entry)
async def get(id: int, db: Session = Depends(get_db)):
    entry = crud.entry.get_entry_id(db=db, entry_id=id)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry


@router.get("/get_last_entry", status_code=200, response_model=schema.Entry)
async def get_last_entry(db: Session = Depends(get_db)):
    entry = crud.entry.get_entries(db=db).pop()
    if not entry:
        raise HTTPException(
            status_code=404, detail="there are no entries in the system"
        )
    return entry


@router.get("/show_fixed_entries", response_model=list[dict[str, Any]], status_code=200)
async def show_fixed_entries():
    """any duplicate should be removed from the file: fixed_entries.jsonl"""
    result = []
    with jsonlines.open("fixed_entries.jsonl") as reader:
        for fixed in reader:
            result.append(fixed)
    return result


@router.get(
    "/show_regular_entries_for_period",
    response_model=list[schema.Entry],
    status_code=200,
)
async def show_regular_entries(
    db: Session = Depends(get_db), period: Period = Depends(get_current_period)
):
    regular = crud.entry.get_regular_entries(db=db, period_nr=int(period.nr))
    if len(regular) == 0:
        raise HTTPException(
            status_code=400, detail="There no regular entries yet for this period"
        )
    return regular
