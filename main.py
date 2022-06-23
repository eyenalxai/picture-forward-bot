import logging
import traceback
from time import sleep
from typing import Optional

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ChatMemberOwner, ChatMemberAdministrator
from aiogram.types.base import Integer
from aiogram.utils import executor
from aiogram.utils.exceptions import BotBlocked, BadRequest

from config.app import API_TOKEN, CHANNEL_ID, SOURCE_URL, CHAT_ID, ENVIRONMENT, SLEEPING_TIME
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


@dp.message_handler(commands=["save"], is_reply=True, chat_id=CHAT_ID)
async def forward_content(message: types.Message) -> Optional[Message]:
    # Get user id from message
    user_id: Integer = message.from_user.id

    # Get all administrators and creator of current chat from message
    admins: list[ChatMemberOwner | ChatMemberAdministrator] = await message.chat.get_administrators()

    # If user is not an admin or creator of current chat, or is not replying to his own message, return None
    if user_id not in [admin.user.id for admin in admins] and message.reply_to_message.from_user.id != user_id:
        return None

    # Check that replied message is a photo
    if message.reply_to_message.photo:
        # Get the largest photo
        largest_photo = find_largest_photo(message.reply_to_message.photo)

        # Send the largest photo to the specified channel id
        return await bot.send_photo(CHANNEL_ID, largest_photo.file_id)

    if message.reply_to_message.video:
        # Send the video to the specified channel id
        return await bot.send_video(CHANNEL_ID, message.reply_to_message.video.file_id)

    if message.reply_to_message.document:
        # Send the document to the specified channel id
        return await bot.send_document(CHANNEL_ID, message.reply_to_message.document.file_id)

    return None


if __name__ == '__main__':
    if ENVIRONMENT == "PROD":
        logging.info("Running in PROD environment")
        logging.info(f"Sleeping for {SLEEPING_TIME} seconds...")

        # Waiting for previous instance to stop
        sleep(SLEEPING_TIME)

    logging.info("Starting up..")
    executor.start_polling(dp, skip_updates=False)
