from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Content


async def is_already_saved(async_session: AsyncSession, file_unique_id: str) -> bool:
    result = await async_session.execute(
        select(Content).where(Content.file_unique_id == file_unique_id)
    )

    return result.scalars().first() is not None


async def save_content_to_database(
    async_session: AsyncSession, file_unique_id: str
) -> None:
    async_session.add(Content(file_unique_id=file_unique_id))
