import asyncio
from datetime import datetime
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy import NullPool, insert
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from src import Base
from src.auth.base_config import current_superuser, current_user
from src.auth.models import User, employee
from src.config import DB_USER_TEST, DB_NAME_TEST, DB_PASS_TEST, DB_PORT_TEST, DB_HOST_TEST
from src.database import get_async_session
from src.employee_position_level.models import employee_position_level
from src.employee_progression.models import employee_progression
from src.main import app

DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"

metadata = Base.metadata

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
metadata.bind = engine_test


user = User(
    id=1,
    email="user@example.com",
    username="user",
    hashed_password="password",
    is_active=True,
    is_verified=True,
    is_superuser=True,
)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@pytest.fixture
async def superuser_client():
    app.dependency_overrides[current_superuser] = lambda: user
    async with AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client


@pytest.fixture
async def current_user_client():
    app.dependency_overrides[current_user] = lambda: user
    async with AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client
