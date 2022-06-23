import logging
import traceback
from typing import Optional

from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatMember, Message
from aiogram.utils.exceptions import BotBlocked, BadRequest
from aiogram.utils.executor import start_webhook

from config import API_TOKEN, CHANNEL_ID, WEBHOOK_URL, WEBHOOK_URL_PATH, HOST, PORT, SOURCE_URL
from util import find_largest_photo

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start", "help"])
async def hello(message: types.Message):
    try:
        await message.reply(
            f"Hello!\n"
            f"If you're an admin, reply with a /save command to forward picture to a meme channel.\n\n"
            f"Source: {SOURCE_URL}"
        )
    except BotBlocked:
        logging.error("Bot is blocked by user")
        return None
    except BadRequest:
        # log exception traceback with error log level
        logging.error(traceback.format_exc())


@dp.message_handler(commands=["save"])
async def save_photo(message: types.Message) -> Optional[Message]:
    user: ChatMember = await bot.get_chat_member(message.chat.id, message.from_user.id)

    # Check that user is admin
    if user.status != "creator" and user.status != "administrator":
        return None

    # Check that replied message is a photo
    if not message.reply_to_message or not message.reply_to_message.photo:
        return None

    # Get the largest photo
    largest_photo = find_largest_photo(message.reply_to_message.photo)

    # Send the largest photo to the specified channel id
    await bot.send_photo(CHANNEL_ID, largest_photo.file_id)


async def on_startup(_):
    logging.info("Starting up..")
    await bot.set_webhook(WEBHOOK_URL)
    logging.info("Webhook set!")


async def on_shutdown(_):
    logging.warning("Shutting down..")

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    logging.warning("Bye!")


if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_URL_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=HOST,
        port=PORT
    )
