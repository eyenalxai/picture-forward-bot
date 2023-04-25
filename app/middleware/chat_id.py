from collections.abc import Awaitable, Callable
from typing import Any

from aiogram.types import Message, TelegramObject

from app.config.log import logger


async def filter_chat_id(
    handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
    message: TelegramObject,
    data: dict[str, Any],
) -> Any:
    if not isinstance(message, Message):
        raise TypeError("message is not a Message")

    if message.chat.id != data["chat_id"]:
        logger.info(
            "Message from {chat_id} is not allowed".format(chat_id=message.chat.id),
        )
        return None

    return await handler(message, data)
