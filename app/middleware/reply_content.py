from collections.abc import Awaitable, Callable
from typing import Any

from aiogram.types import Message, TelegramObject

from app.util.photo import get_largest_picture


async def filter_non_reply_content(  # noqa: CFQ004
    handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
    message: TelegramObject,
    data: dict[str, Any],
) -> Any:
    if not isinstance(message, Message):
        raise TypeError("message is not a Message")

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

    raise ValueError("No file found")
