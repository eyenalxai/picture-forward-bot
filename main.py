import logging
from typing import Optional

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ChatMember, Message

from config import API_TOKEN, CHANNEL_ID
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


@dp.message_handler(commands=['save'])
async def save_photo(message: types.Message) -> Optional[Message]:
    user: ChatMember = await bot.get_chat_member(message.chat.id, message.from_user.id)

    # Check that user is admin
    if user.status != 'creator' and user.status != 'administrator':
        return None

    # Check that replied message is a photo
    if not message.reply_to_message.photo:
        return None

    # Get the largest photo
    largest_photo = find_largest_photo(message.reply_to_message.photo)

    # Send the largest photo to the specified channel id
    await bot.send_photo(CHANNEL_ID, largest_photo.file_id)


# Start the executor to start polling
executor.start_polling(dp, skip_updates=True)
