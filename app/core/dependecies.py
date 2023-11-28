from typing import AsyncGenerator

from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.auth import schema as token_schema
from app.auth.jwt import ALGORITHM, SECRET_KEY, credentials_exception, oauth2_scheme
from app.core.database import SessionLocal
from app.models.models import User
from app.period import crud as period_crud
# from app.core.auth import credentials_exception, oauth2_scheme, SECRET_KEY, ALGORITHM
from app.user import crud as user_crud


async def get_db() -> AsyncGenerator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = token_schema.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = user_crud.user.get_user_by_email(db=db, email=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_super_user(user: User = Depends(get_current_user)) -> User:
    if not user.super_user:
        raise HTTPException(
            status_code=400,
            detail=f"{user.name} has not enough priviledges to perform this operation",
        )
    return user


async def get_current_period(db: Session = Depends(get_db)):
    period = period_crud.period.get_current_period(db=db)
    if period is None:
        raise HTTPException(
            status_code=400,
            detail='period not found'
        )
    return period
