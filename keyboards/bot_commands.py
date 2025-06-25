from aiogram import Bot
from aiogram.types import BotCommand


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Start the bot and get a welcome message"),
        BotCommand(command="animal", description="Get a random animal picture"),
        BotCommand(command="help", description="Show help and available commands"),
        BotCommand(command="about", description="Information about this bot")
    ]
    await bot.set_my_commands(commands)
