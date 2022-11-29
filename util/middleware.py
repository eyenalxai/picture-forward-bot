from typing import Any, Dict, Awaitable, Callable

from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from util.log import logger
from util.photo import get_largest_picture


async def get_async_database_session(
    handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
    message: Message,
    data: Dict[str, Any],
) -> Any:
    try:
        async with AsyncSession(bind=data["async_engine"]) as async_session:
            async with async_session.begin():
                data["async_session"] = async_session
                return await handler(message, data)
    except Exception as e:  # pylint: disable=invalid-name, broad-except
        logger.error(f"Error: {e}")
        return None


async def filter_non_reply_to_user(
    handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
    message: Message,
    data: Dict[str, Any],
) -> Any:

    if not message.from_user or not message.reply_to_message or not message.reply_to_message.from_user:
        return None

    data["reply_to_user"] = message.reply_to_message.from_user
    data["sent_by_user"] = message.from_user
    return await handler(message, data)


async def filter_non_reply_photo(
    handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
    message: Message,
    data: Dict[str, Any],
) -> Any:
    if not message.reply_to_message or not message.reply_to_message.photo:
        return None

    largest_photo = get_largest_picture(pictures=message.reply_to_message.photo)

    data["picture"] = largest_photo
    return await handler(message, data)


async def filter_non_reply_video(
    handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
    message: Message,
    data: Dict[str, Any],
) -> Any:
    if not message.reply_to_message or not message.reply_to_message.video:
        return None

    data["video"] = message.reply_to_message.video
    return await handler(message, data)
