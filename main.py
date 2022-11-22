from aiogram import Dispatcher, Bot, Router, F as MagicFilter
from aiogram.filters import Command
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram.types import Message, PhotoSize, User as TelegramUser, Video
from aiogram.webhook.aiohttp_server import setup_application, SimpleRequestHandler
from aiohttp import web
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine

from models import Base
from settings_reader import PollType
from util.content import handle_content
from util.log import logger
from util.middleware import (
    filter_non_reply_photo,
    filter_non_reply_to_user,
    get_async_database_session,
    filter_non_reply_video,
)
from util.user import is_allowed_user

start_router = Router(name="oof")
picture_router = Router(name="picture router")
video_router = Router(name="video router")


@start_router.message(Command("start", "help"))
async def start(message: Message, description: str) -> None:
    await message.reply(f"{description}", parse_mode="Markdown")


@picture_router.message(Command("save"), MagicFilter.reply_to_message.photo)
async def handle_picture(
    message: Message,
    async_session: AsyncSession,
    reply_to_user: TelegramUser,
    sent_by_user: TelegramUser,
    bot: Bot,
    picture: PhotoSize,
    channel_name: str,
) -> None:
    if not await is_allowed_user(message=message, bot=bot, reply_to_user=reply_to_user, sent_by_user=sent_by_user):
        return None

    await handle_content(
        async_session=async_session,
        bot=bot,
        file=picture,
        channel_name=channel_name,
    )


@video_router.message(Command("save"), MagicFilter.reply_to_message.video)
async def handle_video(
    message: Message,
    async_session: AsyncSession,
    reply_to_user: TelegramUser,
    sent_by_user: TelegramUser,
    bot: Bot,
    video: Video,
    channel_name: str,
) -> None:
    if not await is_allowed_user(message=message, bot=bot, reply_to_user=reply_to_user, sent_by_user=sent_by_user):
        return None

    await handle_content(
        async_session=async_session,
        bot=bot,
        file=video,
        channel_name=channel_name,
    )


async def on_startup(bot: Bot, dispatcher: Dispatcher) -> None:
    from settings_reader import settings

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
        logger.info(f"Webhook set to: {webhook_url}")


async def on_shutdown() -> None:
    logger.info("Shutting down...")


def main() -> None:
    from settings_reader import settings

    dispatcher = Dispatcher(events_isolation=SimpleEventIsolation())

    dispatcher.startup.register(on_startup)
    dispatcher.shutdown.register(on_shutdown)

    dispatcher.include_router(start_router)
    dispatcher.include_router(picture_router)
    dispatcher.include_router(video_router)

    picture_router.message.middleware(filter_non_reply_to_user)  # type: ignore
    picture_router.message.middleware(get_async_database_session)  # type: ignore
    picture_router.message.middleware(filter_non_reply_photo)  # type: ignore

    video_router.message.middleware(filter_non_reply_to_user)  # type: ignore
    video_router.message.middleware(get_async_database_session)  # type: ignore
    video_router.message.middleware(filter_non_reply_video)  # type: ignore

    dispatcher["async_engine"] = create_async_engine(url="sqlite+aiosqlite:///:memory:")
    dispatcher["channel_name"] = settings.channel_name
    dispatcher["description"] = settings.description

    bot = Bot(settings.api_token, parse_mode="HTML")

    if settings.poll_type == PollType.WEBHOOK:
        from aiohttp_healthcheck import HealthCheck  # type: ignore

        health = HealthCheck()

        app = web.Application()
        SimpleRequestHandler(dispatcher=dispatcher, bot=bot).register(app, path=settings.main_bot_path)
        setup_application(app, dispatcher, bot=bot)

        app.add_routes([web.get("/health", health)])

        web.run_app(app, host="0.0.0.0", port=settings.port)

    if settings.poll_type == PollType.POLLING:
        dispatcher.run_polling(bot, skip_updates=True)


if __name__ == "__main__":
    main()
