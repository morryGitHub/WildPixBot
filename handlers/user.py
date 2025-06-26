import os
import random

import aiohttp
from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()
user = Router()

CATS = os.getenv("CAT")
DOGS = os.getenv("DOG")
FOXES = os.getenv("FOX")


@user.message(CommandStart())
async def start_command(message: Message):
    await message.answer(
        "👋 Hello! I’m your animal buddy.\nSend /help to see what I can do!"
    )


@user.message(Command('help'))
async def help_command(message: Message):
    await message.answer(
        "🐾 Available commands:\n"
        "/start — Start the bot\n"
        "/animal — Get a random animal\n"
        "/help — Show this help message\n"
        "/about — Info about this bot"
    )


@user.message(Command('animal'))
@user.message()
async def animal_handler(message: Message, bot: Bot):
    animal = random.choice([CATS, DOGS, FOXES])
    async with (aiohttp.ClientSession() as session):
        async with session.get(animal) as response:
            if response.status != 200:
                await message.answer("Ошибка при получении животного 🐾")
                return

            data = await response.json()

            if animal == FOXES:
                url: str | None = data['image']
            elif animal == CATS:
                url = data[0]['url']
            elif animal == DOGS:
                url = data['url']
                if not url:
                    url = f"https://random.dog/{data['woof']}"
            else:
                url = None

            if url:
                if url.endswith((".mp4", ".webm")):
                    await message.answer_video(url,
                                               supports_streaming=True)
                else:
                    await message.answer_photo(url)
            else:
                await bot.send_message(chat_id=os.getenv('OWNER'),
                                       text=f"Помилка в отриманні фотографії у юзера {message.from_user.id} = {message.from_user.username}")
                await message.answer("Не удалось получить изображение 😿")
