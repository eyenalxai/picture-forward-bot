from aiogram import Dispatcher, Bot, Router, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram.types import Message, PhotoSize, User as TelegramUser, Video, Animation
from aiogram.webhook.aiohttp_server import setup_application, SimpleRequestHandler
from aiohttp import web
from aiohttp_healthcheck import HealthCheck  # type: ignore
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine

from models import Base
from settings_reader import PollType
from settings_reader import settings
from util.content import post_content_to_channel, get_file
from util.log import logger
from util.middleware import (
    filter_chat_id,
    filter_non_reply_to_user,
    get_async_database_session,
    filter_non_reply_content,
)
from util.query.content import is_already_saved
from util.user import is_allowed_user

start_router = Router(name="oof")
content_router = Router()


@start_router.message(Command("start", "help"))
async def start(message: Message, description: str) -> None:
    await message.reply(f"{description}", parse_mode="Markdown")


@content_router.message(Command("save"), F.reply_to_message)
async def handle_content(  # noqa: CFQ002
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
        message=message, bot=bot, reply_to_user=reply_to_user, sent_by_user=sent_by_user
    ):
        return

    sticker_file: Video | PhotoSize | Animation = get_file(
        video=video, picture=picture, animation=animation
    )

    if await is_already_saved(
        async_session=async_session, file_unique_id=sticker_file.file_unique_id
    ):
        return

    await post_content_to_channel(
        bot=bot,
        sticker_file=sticker_file,
        channel_name=channel_name,
        async_session=async_session,
    )


async def on_startup(bot: Bot, dispatcher: Dispatcher) -> None:

    async_engine = dispatcher["async_engine"]

    assert async_engine is not None
    assert isinstance(async_engine, AsyncEngine)

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        logger.info("Dropped all tables")
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Created all tables")

    if settings.poll_type == PollType.WEBHOOK:
        webhook_url = settings.webhook_url
        await bot.set_webhook(webhook_url)
        logger.info("Webhook set to: %s", webhook_url)


async def on_shutdown() -> None:
    logger.info("Shutting down...")


def main() -> None:

    dispatcher = Dispatcher(events_isolation=SimpleEventIsolation())

    dispatcher.startup.register(on_startup)
    dispatcher.shutdown.register(on_shutdown)

    dispatcher.include_router(start_router)
    dispatcher.include_router(content_router)

    dispatcher.message.middleware(filter_chat_id)  # type: ignore

    content_router.message.middleware(filter_non_reply_to_user)  # type: ignore
    content_router.message.middleware(filter_non_reply_content)  # type: ignore
    content_router.message.middleware(get_async_database_session)  # type: ignore

    dispatcher["async_engine"] = create_async_engine(url="sqlite+aiosqlite:///:memory:")
    dispatcher["channel_name"] = settings.channel_name
    dispatcher["description"] = settings.description
    dispatcher["chat_id"] = settings.chat_id

    bot = Bot(settings.api_token, parse_mode="HTML")

    if settings.poll_type == PollType.WEBHOOK:

        health = HealthCheck()

        app = web.Application()
        SimpleRequestHandler(dispatcher=dispatcher, bot=bot).register(
            app, path=settings.main_bot_path
        )
        setup_application(app, dispatcher, bot=bot)

        app.add_routes([web.get("/health", health)])

        web.run_app(app, host="0.0.0.0", port=settings.port)

    if settings.poll_type == PollType.POLLING:
        dispatcher.run_polling(bot, skip_updates=True)


if __name__ == "__main__":
    main()
