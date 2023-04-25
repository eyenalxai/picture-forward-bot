from aiogram import Dispatcher
from aiogram.fsm.storage.memory import SimpleEventIsolation
from sqlalchemy.ext.asyncio import create_async_engine

from app.middleware.chat_id import filter_chat_id
from app.middleware.database import get_async_database_session
from app.middleware.reply_content import filter_non_reply_content
from app.middleware.reply_to_user import filter_non_reply_to_user
from app.route.content import content_router
from app.util.lifecycle import on_shutdown, on_startup
from app.util.settings import bot_settings


def initialize_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher(events_isolation=SimpleEventIsolation())

    dispatcher.startup.register(on_startup)
    dispatcher.shutdown.register(on_shutdown)

    dispatcher.include_router(content_router)

    dispatcher.message.middleware(filter_chat_id)

    content_router.message.middleware(filter_non_reply_to_user)
    content_router.message.middleware(filter_non_reply_content)
    content_router.message.middleware(get_async_database_session)

    dispatcher["async_engine"] = create_async_engine(url="sqlite+aiosqlite:///:memory:")
    dispatcher["channel_name"] = bot_settings.channel_name
    dispatcher["chat_id"] = bot_settings.chat_id

    return dispatcher
