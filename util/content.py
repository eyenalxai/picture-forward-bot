from aiogram import Bot
from aiogram.types import Video, PhotoSize, Animation
from sqlalchemy.ext.asyncio import AsyncSession

from util.query.content import save_content_to_database


def get_file(
    video: Video | None = None,
    picture: PhotoSize | None = None,
    animation: Animation | None = None,
) -> Video | PhotoSize | Animation:
    if video is not None:
        return video

    if picture is not None:
        return picture

    if animation is not None:
        return animation

    raise Exception("No file found")


async def post_content_to_channel(
    async_session: AsyncSession,
    bot: Bot,
    channel_name: str,
    sticker_file: Video | PhotoSize | Animation,
) -> None:

    await save_content_to_database(
        async_session=async_session, file_unique_id=sticker_file.file_unique_id
    )

    if isinstance(sticker_file, PhotoSize):
        await bot.send_photo(chat_id=channel_name, photo=sticker_file.file_id)
        return

    if isinstance(sticker_file, Video):
        await bot.send_video(chat_id=channel_name, video=sticker_file.file_id)
        return

    if isinstance(sticker_file, Animation):
        await bot.send_animation(chat_id=channel_name, animation=sticker_file.file_id)
        return
