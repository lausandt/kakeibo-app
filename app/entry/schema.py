from datetime import date
from enum import Enum

from pydantic import BaseModel, Field


class Interval(str, Enum):
    weekly: str = "Weekly"
    four_weekly: str = "Four weekly"
    monthly: str = "Monthly"
    quarterly: str = "Quarterly"
    yearly: str = "Yearly"


class EntryBase(BaseModel):
    title: str
    amount: int | float = Field(gt=0, description="The amount must be greater than 0")
    description: str = Field(title="The description of the entry", max_length=300)
    supplier: str = Field(title="The supplier", max_length=300)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Shopping",
                    "amount": 37.09,
                    "description": "groceries",
                    "supplier": "lidl",
                }
            ]
        }
    }


class EntryCreate(EntryBase):
    entry_date: date = date.today()


class FixedEntryCreate(EntryBase):
    entry_date: date | None = None
    interval: Interval
    url: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "volkskrant",
                    "amount": 16.67,
                    "description": "newspaper",
                    "supplier": "DPG media",
                    "interval": "Four weekly",
                    "url": "volkskrant.nl",
                }
            ]
        }
    }


class Entry(EntryCreate):
    id: int
    owner_id: int
    period_id: int | None

    class ConfigDict:
        from_attributes = True
        string_to_lower = True


class FixedEntry(FixedEntryCreate):
    id: int
    owner_id: int
    period_id: int | None

    class ConfigDict:
        from_attributes = True
        string_to_lower = True
