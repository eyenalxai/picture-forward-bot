from collections.abc import Awaitable, Callable
from typing import Any

from aiogram.types import Message, TelegramObject


async def filter_non_reply_to_user(
    handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
    message: TelegramObject,
    data: dict[str, Any],
) -> Any:
    if not isinstance(message, Message):
        raise TypeError("message is not a Message")

    if (
        not message.from_user
        or not message.reply_to_message
        or not message.reply_to_message.from_user
    ):
        return None

    data["reply_to_user"] = message.reply_to_message.from_user
    data["sent_by_user"] = message.from_user
    return await handler(message, data)
