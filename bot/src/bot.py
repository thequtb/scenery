import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Bot token from environment variable
API_TOKEN = os.getenv('TELEGRAM_API_KEY')

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    """Handler for /start command"""
    await message.answer(f"Hello, {message.from_user.full_name}! I'm an echo bot. Send me any message and I'll repeat it.")

@dp.message()
async def echo_message(message: Message):
    """Handler for all other messages"""
    await message.answer(message.text)

async def main():
    # Start the bot
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main()) 