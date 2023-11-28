from pydantic import BaseModel, EmailStr

from app.entry.schema import Entry


class UserBase(BaseModel):
    name: str
    full_name: str | None
    email: EmailStr


class UserUpdate(UserBase):
    ...


class UserCreate(UserBase):
    password: str
    super_user: bool = False

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "agent.provocateur@testmail.com",
                    "full_name": "Agent Provocateur",
                    "name": "Agent",
                    "password": "string",
                    "super_user": "false",
                }
            ]
        }
    }


class User(UserCreate):
    id: int
    active: bool = True

    entries: list[Entry] = []

    class ConfigDict:
        from_attributes = True
