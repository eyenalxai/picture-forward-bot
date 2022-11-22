from typing import Any, Dict, Awaitable, Callable

from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from util.log import logger
from util.photo import get_largest_picture


async def filter_chat_id(
    handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
    message: Message,
    data: Dict[str, Any],
) -> Any:
    if message.chat.id != data["chat_id"]:
        logger.info(f"Message from {message.chat.id} is not allowed")
        return None

    return await handler(message, data)


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
    except Exception as e:
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


async def filter_non_reply_content(
    handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
    message: Message,
    data: Dict[str, Any],
) -> Any:
    if not message.reply_to_message:
        return None

    if message.reply_to_message.video:
        data["video"] = message.reply_to_message.video
        return await handler(message, data)
    if message.reply_to_message.animation:
        data["animation"] = message.reply_to_message.animation
        return await handler(message, data)
    if message.reply_to_message.photo:
        data["picture"] = get_largest_picture(pictures=message.reply_to_message.photo)
        return await handler(message, data)
