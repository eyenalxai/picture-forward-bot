import logging
import traceback
from time import sleep
from typing import Optional

import sqlalchemy
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils.exceptions import BotBlocked, BadRequest
from aiogram.utils.executor import start_webhook

from config.app import API_TOKEN, CHANNEL_ID, CHAT_ID, ENVIRONMENT, SLEEPING_TIME, DESCRIPTION, WEBHOOK_PATH, \
    WEBHOOK_URL, PORT
from config.database import metadata, DATABASE_URL
from util import find_largest_photo, is_already_saved, save_file_id, is_allowed_user

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
            f"{DESCRIPTION}",
            parse_mode="Markdown"
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
    if not await is_allowed_user(message):
        return None

    # Check that replied message is a photo
    if message.reply_to_message.photo:
        # Get the largest photo
        largest_photo = find_largest_photo(message.reply_to_message.photo)

        # Check that photo is not already saved in database, if it is, return None
        if await is_already_saved(largest_photo.file_id):
            logging.info(f"Photo {largest_photo.file_id} is already saved")
            return None

        # Save largest photo file id to database
        await save_file_id(largest_photo.file_id)

        # Send the largest photo to the specified channel id
        return await bot.send_photo(CHANNEL_ID, largest_photo.file_id)

    if message.reply_to_message.video:
        # Check that video is not already saved in database, if it is, return None
        if await is_already_saved(message.reply_to_message.video.file_id):
            logging.info(f"Video {message.reply_to_message.video.file_id} is already saved")
            return None

        # Save video file id to database using ormar
        await save_file_id(message.reply_to_message.video.file_id)

        # Send the video to the specified channel id
        return await bot.send_video(CHANNEL_ID, message.reply_to_message.video.file_id)

    if message.reply_to_message.document:
        # Check that document is not already saved in database, if it is, return None
        if await is_already_saved(message.reply_to_message.document.file_id):
            logging.info(f"Document {message.reply_to_message.document.file_id} is already saved")
            return None

        # Save document file id to database using ormar
        await save_file_id(message.reply_to_message.document.file_id)

        # Send the document to the specified channel id
        return await bot.send_document(CHANNEL_ID, message.reply_to_message.document.file_id)

    return None


async def on_startup(dp):
    logging.info("Starting up...")

    # Create the database
    logging.info("Initializing database...")
    engine = sqlalchemy.create_engine(DATABASE_URL)

    # Just to be sure we clear the db before
    logging.info("Dropping existing database...")
    metadata.drop_all(engine)

    logging.info("Creating database...")
    metadata.create_all(engine)

    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    logging.warning('Bye!')


if __name__ == '__main__':

    if ENVIRONMENT == "PROD":
        logging.info("Running in PROD environment")
        logging.info(f"Sleeping for {SLEEPING_TIME} seconds...")

        # Waiting for previous instance to stop
        sleep(SLEEPING_TIME)

    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        skip_updates=False,
        host="0.0.0.0",
        port=PORT,
    )
