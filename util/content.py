from aiogram import Bot
from aiogram.types import Video, PhotoSize
from sqlalchemy.ext.asyncio import AsyncSession

from util.query.content import save_content_to_database, is_already_saved


async def handle_content(
    async_session: AsyncSession,
    bot: Bot,
    file: PhotoSize | Video,
    channel_name: str,
) -> None:
    if await is_already_saved(
        async_session=async_session, file_unique_id=file.file_unique_id
    ):
        return

    await save_content_to_database(
        async_session=async_session, file_unique_id=file.file_unique_id
    )

    if isinstance(file, PhotoSize):
        await bot.send_photo(chat_id=channel_name, photo=file.file_id)
        return

    if isinstance(file, Video):
        await bot.send_video(chat_id=channel_name, video=file.file_id)
        return
