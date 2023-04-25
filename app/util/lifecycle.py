from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from app.config.log import logger
from app.models.models import Base
from app.util.health_check import health_check_endpoint
from app.util.settings import bot_settings


async def on_startup(bot: Bot, dispatcher: Dispatcher) -> None:
    async_engine = dispatcher["async_engine"]

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        logger.info("Dropped all tables")
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Created all tables")

    if bot_settings.poll_type == "WEBHOOK":
        webhook_url = bot_settings.webhook_url
        await bot.set_webhook(webhook_url)
        logger.info("Webhook set to: {webhook_url}".format(webhook_url=webhook_url))


async def on_shutdown() -> None:
    logger.info("Shutting down...")


def start_bot(*, dispatcher: Dispatcher, bot: Bot) -> None:
    if bot_settings.poll_type == "WEBHOOK":
        app = web.Application()
        SimpleRequestHandler(dispatcher=dispatcher, bot=bot).register(
            app,
            path=bot_settings.main_bot_path,
        )
        setup_application(app, dispatcher, bot=bot)
        app.add_routes([web.get("/health", health_check_endpoint)])
        web.run_app(app, host=bot_settings.host, port=bot_settings.port)

    if bot_settings.poll_type == "POLLING":
        dispatcher.run_polling(bot, skip_updates=True)
