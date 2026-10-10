import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.init_db import init_models
from app.main import app


@pytest_asyncio.fixture(scope="session", loop_scope="session", autouse=True)
async def _create_tables():
    await init_models()


@pytest_asyncio.fixture(loop_scope="session")
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c