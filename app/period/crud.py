from dataclasses import dataclass
from datetime import date

import jsonlines
from sqlalchemy.orm import Session

from app.entry.crud import entry
from app.models.models import Period

from . import schema


@dataclass
class PeriodCRUD:
    model: type[Period]

    def create_period(self, *, db: Session, period: schema.PeriodCreate) -> Period:
        db_period = Period(**period.model_dump())
        db.add(db_period)
        db.commit()
        db.refresh(db_period)
        return db_period

    def load_fixed_for_period(
        self, *, db: Session, period: Period, owner_id: int
    ) -> Period:
        entry.remove_fixeds_for_period(db, period_nr=int(period.nr))  
        with jsonlines.open("fixed_entries.jsonl") as reader:
            for obj in reader:
                obj["entry_date"] = period.start_date
                obj["period_id"] = period.nr
                entry.create_fixed_entry(db=db, entry=obj, owner_id=owner_id)
            return period

    def load_loose_entries_for_period(self, *, db: Session, period: Period) -> Period:
        entries = entry.get_entries(db=db)
        loose = list(filter(lambda x: x.interval is None, entries))
        period.entries += loose
        return period

    def update_period(
        self, *, db: Session, period: schema.PeriodCreate
    ) -> Period | None:
        db_period = db.query(self.model).filter(self.model.nr == period.nr).first()
        db.delete(db_period)
        db.commit()
        new_period = self.create_period(db=db, period=period)
        return new_period

    def get_current_period(self, *, db: Session) -> Period | None:
        d = date.today()
        period = (
            db.query(self.model)
            .filter(self.model.start_date <= d, self.model.end_date <= d)
            .first()
        )
        return period

    def delete_period(self, *, db: Session, nr: int) -> Period | None:
        db_period = db.query(self.model).filter(self.model.nr == nr).first()
        db.delete(db_period)
        db.commit()
        return db_period

    def get_period_by_number(self, *, db: Session, nr: int) -> None | Period:
        per = db.query(self.model).filter(self.model.nr == nr).first()
        return per


period = PeriodCRUD(Period)
