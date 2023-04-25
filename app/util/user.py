from aiogram import Bot
from aiogram.types import Message
from aiogram.types import User as TelegramUser


async def is_allowed_user(
    *,
    message: Message,
    bot: Bot,
    reply_to_user: TelegramUser,
    sent_by_user: TelegramUser,
) -> bool:
    admins = await bot.get_chat_administrators(message.chat.id)

    return reply_to_user.id == sent_by_user.id or sent_by_user.id in {
        admin.user.id for admin in admins
    }
