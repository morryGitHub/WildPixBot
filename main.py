import asyncio
import os
import logging

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers.last_command import process_last_pending_update
from handlers.user import user
from keyboards.bot_commands import set_commands


async def main():
    load_dotenv()
    bot = Bot(os.getenv("API_TOKEN"))

    await set_commands(bot)

    dp = Dispatcher()
    dp.include_router(user)

    await process_last_pending_update(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s] #%(levelname)-8s %(filename)s:'
                               '%(lineno)d - %(name)s - %(message)s',
                        style="{")
    logger = logging.getLogger()

    print("Bot is running")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
