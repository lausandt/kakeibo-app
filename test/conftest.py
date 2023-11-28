from typing import Any, Generator

import pytest
from fastapi.testclient import TestClient

from app.__main__ import app
from app.auth.jwt import create_access_token
from app.core.dependecies import get_current_active_super_user, get_current_period  # get_current_user
from app.models.models import User, Period


async def override_get_current_active_superuser():

    stub = {
        "name": "user",
        "full_name": "test user",
        "email": "test.user@example.com",
        "password": "string",
        "super_user": "true",
        "active": "true",
        "id": 100,
        "entries": [],
    }

    user = User(**stub)
    return user

async def override_get_current_period():
    stub = {
        'nr':1000,
        'start_date':2023-10-23,
        'end_date':2023-11-22,
        'entries': []
    }
    period = Period(**stub)
    return period


@pytest.fixture
def client() -> Generator:
    with TestClient(app) as client:
        app.dependency_overrides[
            get_current_active_super_user
        ] = override_get_current_active_superuser
        app.dependency_overrides[
             get_current_period
         ] = override_get_current_period
        yield client
        app.dependency_overrides = {}

@pytest.fixture
def user_in() -> dict[str, Any]:
    stub = {
        "name": "agent provocateur",
        "full_name": "Test Agent",
        "email": "agent.test@example.com",
        "password": "string",
        "super_user": "false",
    }
    return stub


@pytest.fixture
def user_out() -> dict[str, Any]:
    stub = {
        "name": "agent provocateur",
        "full_name": "Test Agent",
        "email": "agent.test@example.com",
        "password": "string",
        "super_user": False,
        "active": True,
        "id": 1_000_000,
        "entries": [],
    }
    return stub

@pytest.fixture
def user_access_token() -> Any:
    return create_access_token({'sub': "agent.test@example.com"})

@pytest.fixture
def entry_in() -> dict[str, Any]:
    stub = {
        "amount": 28.89,
        "description": "Cote du Boeuf",
        "supplier": "butcher",
        "title": "Shopping",
    }
    return stub


@pytest.fixture
def entry_out() -> dict[str, Any]:
    stub = {
        "title": "Shopping",
        "amount": 28.89,
        "description": "Cote du Boeuf",
        "supplier": "butcher",
        "entry_date": "",
        "id": 0,
        "owner_id": 3,
    }
    return stub

