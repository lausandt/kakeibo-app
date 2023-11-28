from dataclasses import dataclass
from typing import Any

import jsonlines
from sqlalchemy.orm import Session

from app.models.models import Entry
from app.period.schema import Period

from .schema import EntryCreate, FixedEntryCreate


@dataclass
class EntryCRUD:
    """
    Entry crud class with methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
    """

    model: type[Entry]

    def create_entry(
        self, *, db: Session, entry: EntryCreate, owner_id: int, period_id: int
    ) -> Entry:
        db_entry = Entry(**entry.model_dump(), owner_id=owner_id, period_id=period_id)
        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)
        return db_entry

    def create_fixed_entry_json(self, *, entry: FixedEntryCreate) -> FixedEntryCreate:
        """persistently store the fixed entries as json line, so they can be loaded periodically"""
        with jsonlines.open("fixed_entries.jsonl", "a") as writer:
            writer.write(entry.model_dump())
        return entry

    def create_fixed_entry(
        self, *, db: Session, entry: dict[str, Any], owner_id: int
    ) -> Entry:
        db_entry = Entry(**entry, owner_id=owner_id)
        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)
        return db_entry

    def get_entries(
        self, *, db: Session, skip: int = 0, limit: int = 100
    ) -> list[Entry]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_regular_entries(self, *, db: Session, period_nr: int) -> list[Entry]:
        entries = db.query(self.model).filter(self.model.period_id == period_nr)
        return [e for e in entries if not e.interval]

    def get_entry_id(self, *, db: Session, entry_id: int) -> Entry | None:
        return db.query(self.model).filter(self.model.id == entry_id).first()

    def get_entries_by_period(self, *, db: Session, period: Period) -> list[Entry]:
        return [
            e
            for e in self.get_entries(db=db)
            if period.start_date <= e.entry_date < period.end_date
        ]

    def remove(self, db: Session, *, entry_id: int) -> Entry | None:
        db_entry = db.query(self.model).filter(self.model.id == entry_id).first()
        db.delete(db_entry)
        db.commit()
        return db_entry

    def remove_fixed(self, *, db: Session, id: int) -> Entry | None:
        db_entry = db.query(self.model).filter(self.model.id == id).first()
        db.delete(db_entry)
        db.commit()
        return db_entry

    def remove_fixeds_for_period(self, db: Session, period_nr: int) -> None:
        entries = db.query(self.model).filter(self.model.period_id == period_nr).all()
        fixeds = [e for e in entries if e.interval]
        for e in fixeds:
            db.delete(e)
            db.commit()


entry = EntryCRUD(model=Entry)
