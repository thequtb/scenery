import asyncio
import logging
import os
import aiohttp
import json
import uuid
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
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000')

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Store user conversations
user_conversations = {}

@dp.message(CommandStart())
async def cmd_start(message: Message):
    """Handler for /start command"""
    await message.answer(f"Hello, {message.from_user.full_name}! I'm your travel booking assistant. How can I help you plan your next trip?")
    # Reset conversation for this user
    user_conversations.pop(message.from_user.id, None)

@dp.message()
async def handle_message(message: Message):
    """Handle all non-command messages"""
    user_id = message.from_user.id
    conversation_id = user_conversations.get(user_id)
    
    # Prepare the request payload
    payload = {
        'message': message.text
    }
    
    if conversation_id:
        payload['conversation_id'] = conversation_id
    
    # Make API request to our agent service
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_BASE_URL}/api/agents/conversation/", json=payload) as response:
            if response.status == 200:
                data = await response.json()
                
                # Store conversation ID
                user_conversations[user_id] = data.get('conversation_id')
                
                # Check if conversation is complete
                if data.get('is_complete'):
                    # Send the Telegram mini app link
                    await message.answer(f"I've gathered all the information I need. You can now complete your booking.")
                    await message.answer(data.get('telegram_link', 'https://t.me/qnbq_assistant_bot/btravel'))
                    
                    # Clear the conversation
                    user_conversations.pop(user_id, None)
                else:
                    # Send the agent response
                    await message.answer(data.get('message', 'Sorry, I could not process your request.'))
            else:
                # Handle API error
                try:
                    error_data = await response.json()
                    if 'error' in error_data and 'telegram_link' in error_data:
                        # This is an expired conversation
                        await message.answer(f"Your session has expired. Please start a new conversation.")
                        await message.answer(error_data.get('telegram_link'))
                        # Clear the conversation
                        user_conversations.pop(user_id, None)
                    else:
                        await message.answer("Sorry, I'm having trouble processing your request. Please try again later.")
                except:
                    await message.answer("Sorry, I'm having trouble connecting to the service. Please try again later.")

async def main():
    # Start the bot
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main()) 