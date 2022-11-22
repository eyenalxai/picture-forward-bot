from typing import Union, Optional

from aiogram import Bot
from aiogram.types import Video, PhotoSize, Animation
from sqlalchemy.ext.asyncio import AsyncSession

from util.query.content import save_content, is_already_saved


def get_file(
    video: Optional[Video] = None,
    picture: Optional[PhotoSize] = None,
    animation: Optional[Animation] = None,
) -> Union[Video, PhotoSize, Animation]:
    if video is not None:
        return video

    if picture is not None:
        return picture

    if animation is not None:
        return animation

    raise Exception("No file found")


async def save_content_to_channel(
    async_session: AsyncSession,
    bot: Bot,
    channel_name: str,
    video: Optional[Video] = None,
    picture: Optional[PhotoSize] = None,
    animation: Optional[Animation] = None,
) -> None:
    file = get_file(video=video, picture=picture, animation=animation)

    if await is_already_saved(async_session=async_session, file_unique_id=file.file_unique_id):
        return None

    await save_content(async_session=async_session, file_unique_id=file.file_unique_id)

    if isinstance(file, PhotoSize):
        await bot.send_photo(chat_id=channel_name, photo=file.file_id)
        return None

    if isinstance(file, Video):
        await bot.send_video(chat_id=channel_name, video=file.file_id)
        return None

    if isinstance(file, Animation):
        await bot.send_animation(chat_id=channel_name, animation=file.file_id)
        return None
