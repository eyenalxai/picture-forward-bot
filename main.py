from aiogram import Bot

from app.util.dispatcher import initialize_dispatcher
from app.util.lifecycle import start_bot
from app.util.settings import bot_settings


def main() -> None:
    bot = Bot(token=bot_settings.api_token)
    dispatcher = initialize_dispatcher()
    start_bot(dispatcher=dispatcher, bot=bot)


if __name__ == "__main__":
    main()
