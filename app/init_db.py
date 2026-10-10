import asyncio

from app import models  # noqa: F401  (registers the tables)
from app.database import Base, engine


async def init_models() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_models())