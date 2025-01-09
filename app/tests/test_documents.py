import pytest
import pytest_asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.models.models import Base
from app.api.deps import get_session

@pytest_asyncio.fixture(scope="session", autouse=True)
async def test_ingest_document(async_client: AsyncClient):
    response = await async_client.post("/ingest", json={"content": "Test document content"})
    assert response.status_code == 200
    assert response.json()["content"] == "Test document content"

@pytest_asyncio.fixture(scope="session", autouse=True)
async def test_answer_question(async_client: AsyncClient):
    response = await async_client.post("/chat", json={"question": "What is the content?", "document_ids": [1]})
    assert response.status_code == 200
    assert "answer" in response.json()

@pytest_asyncio.fixture(scope="session", autouse=True)
async def test_select_documents(async_client: AsyncClient):
    response = await async_client.post("/select", json={"criteria": {}})
    assert response.status_code == 200