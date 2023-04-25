from aiogram import Bot
from aiogram import F as MagicFilter
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Animation, Message, PhotoSize
from aiogram.types import User as TelegramUser
from aiogram.types import Video
from sqlalchemy.ext.asyncio import AsyncSession

from app.util.content import get_file, post_content_to_channel
from app.util.query import is_already_saved
from app.util.user import is_allowed_user

content_router = Router()


@content_router.message(Command("save"), MagicFilter.reply_to_message)
async def handle_content(
    message: Message,
    async_session: AsyncSession,
    reply_to_user: TelegramUser,
    sent_by_user: TelegramUser,
    bot: Bot,
    channel_name: str,
    video: Video | None = None,
    picture: PhotoSize | None = None,
    animation: Animation | None = None,
) -> None:
    if not await is_allowed_user(
        message=message,
        bot=bot,
        reply_to_user=reply_to_user,
        sent_by_user=sent_by_user,
    ):
        return None

    sticker_file: Video | PhotoSize | Animation = get_file(
        video=video,
        picture=picture,
        animation=animation,
    )

    if await is_already_saved(
        async_session=async_session,
        file_unique_id=sticker_file.file_unique_id,
    ):
        return None

    return await post_content_to_channel(
        bot=bot,
        sticker_file=sticker_file,
        channel_name=channel_name,
        async_session=async_session,
    )
