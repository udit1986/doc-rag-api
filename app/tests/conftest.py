import logging
import os
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
import sqlalchemy
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)

from app.core import database_session
from app.core.config import get_settings
from app.main import app as fastapi_app
from app.models.models import Base


@pytest_asyncio.fixture(scope="session", autouse=True)
async def fixture_setup_new_test_database() -> None:
    worker_name = os.getenv("PYTEST_XDIST_WORKER", "gw0")
    test_db_name = f"test_db_{worker_name}"

    # create new test db using connection to current database
    conn = await database_session._ASYNC_ENGINE.connect()
    await conn.execution_options(isolation_level="AUTOCOMMIT")
    await conn.execute(sqlalchemy.text(f"DROP DATABASE IF EXISTS {test_db_name}"))
    await conn.execute(sqlalchemy.text(f"CREATE DATABASE {test_db_name}"))
    await conn.close()

    session_mpatch = pytest.MonkeyPatch()
    session_mpatch.setenv("DATABASE__DB", test_db_name)
    session_mpatch.setenv("SECURITY__PASSWORD_BCRYPT_ROUNDS", "4")

    # force settings to use now monkeypatched environments
    get_settings.cache_clear()

    # monkeypatch test database engine
    engine = database_session.new_async_engine(get_settings().sqlalchemy_database_uri)

    session_mpatch.setattr(
        database_session,
        "_ASYNC_ENGINE",
        engine,
    )
    session_mpatch.setattr(
        database_session,
        "_ASYNC_SESSIONMAKER",
        async_sessionmaker(engine, expire_on_commit=False),
    )

    # create app tables in test database
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def fixture_clean_get_settings_between_tests() -> AsyncGenerator[None]:
    yield

    get_settings.cache_clear()


@pytest_asyncio.fixture(name="client", scope="function")
async def fixture_client(session: AsyncSession) -> AsyncGenerator[AsyncClient]:
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as aclient:
        aclient.headers.update({"Host": "localhost"})
        yield aclient

