import logging
import traceback
from typing import Optional

from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatMember, Message
from aiogram.utils import executor
from aiogram.utils.exceptions import BotBlocked, BadRequest, TerminatedByOtherGetUpdates

from config import API_TOKEN, CHANNEL_ID, SOURCE_URL
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
    except BadRequest as bad_req_exception:
        if bad_req_exception.text == "Replied message not found":
            logging.error("Message not found")
            return None
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


if __name__ == '__main__':
    logging.info("Starting up..")
    try:
        executor.start_polling(dp, skip_updates=True)
    except TerminatedByOtherGetUpdates:
        logging.error("More than one bot instance is running at the moment.")
