import asyncio
from telebot.async_telebot import AsyncTeleBot
from bl import main
import json
import os
from dotenv import load_dotenv


load_dotenv()
bot = AsyncTeleBot(os.getenv('TOKEN'))


@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    await bot.reply_to(message, 'Hello!')


@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    # request_text = message.text
    await bot.send_message(message.chat.id, await main(message.text))

asyncio.run(bot.polling())
