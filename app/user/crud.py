from dataclasses import dataclass
from typing import Any, Sequence

from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.entry.schema import EntryCreate
from app.models.models import Entry, User

from . import schema


@dataclass
class UserCRUD:
    """
    User crud class with methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
    """

    model: type[User]

    def create_user(self, *, db: Session, user: schema.UserCreate) -> User:
        db_user = User(**user.model_dump())
        #  name = db_user.name
        db_user.name = db_user.name.lower()
        db_user.password = get_password_hash(user.password)  # type: ignore
        db.add(db_user)
        db.commit()
        return db_user

    def get_users(
        self, *, db: Session, skip: int = 0, limit: int = 100
    ) -> Sequence[dict[str, Any]]:
        seq: list[User] = db.query(self.model).offset(skip).limit(limit).all()
        return [{"username": u.name, "email": u.email} for u in seq]

    def get_user_by_email(self, *, db: Session, email: str | None) -> User | None:
        if email is None:
            return None
        return db.query(self.model).filter(self.model.email == email).first()

    def get_user_by_id(self, *, db: Session, id: int) -> User | None:
        return db.query(self.model).filter(self.model.id == id).first()

    def remove(self, *, db: Session, user_id: int) -> User | None:
        user = db.query(self.model).filter(self.model.id == user_id).first()
        db.delete(user)
        db.commit()
        return user

    def create_entry_for_user(
        self, db: Session, entry: EntryCreate, user_id: int, period_id: int
    ) -> Entry:
        db_entry = Entry(**entry.model_dump(), owner_id=user_id, period_id=period_id)
        self.__update_user_entries(db=db, user_id=user_id, entry=db_entry)
        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)
        return db_entry

    def set_active_level(self, *, db: Session, user_id: int) -> User | None:
        user = db.query(self.model).filter(self.model.id == user_id).first()
        if user:
            user.active = not user.active  # type: ignore
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def set_super_user(self, *, db: Session, user_id: int) -> User | None:
        user = db.query(self.model).filter(self.model.id == user_id).first()
        if user:
            user.super_user = True  # type: ignore
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def __update_user_entries(
        self, db: Session, *, user_id: int, entry: Entry
    ) -> User | None:
        user = db.query(self.model).filter(self.model.id == user_id).first()
        if user:
            user.entries.append(entry)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


# user crud object
user = UserCRUD(model=User)
