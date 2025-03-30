import os
import asyncio
from telegram import _bot
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_USER_ID = os.getenv("TELEGRAM_USER_ID")


async def test_bot():
    print(f"Testing bot with token: {TELEGRAM_BOT_TOKEN}")
    print(f"Sending to user ID: {TELEGRAM_USER_ID}")

    try:
        bot = _bot.Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.send_message(
            chat_id=TELEGRAM_USER_ID,
            text="Test message from bot"
        )
        print("Message sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_bot())
