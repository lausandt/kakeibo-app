from datetime import date

from pydantic import BaseModel

from app.entry.schema import Entry


class PeriodCreate(BaseModel):
    nr: int
    start_date: date
    end_date: date

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"nr": 11, "start_date": "2008-09-15", "end_date": "2008-09-16"}
            ]
        }
    }


class Period(PeriodCreate):
    id: int
    entries: list[Entry] = []

    class ConfigDict:
        from_attributes = True
