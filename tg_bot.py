from Private_setting import tg_token

import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

# Токен бота можно получить через https://t.me/BotFather
TOKEN = tg_token

# Создаем экземпляр Dispatcher (Диспетчер) для управления обработчиками событий
dp = Dispatcher()

def tell_the_bot():
    pass

# Обработчик для команды /start
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Этот обработчик получает сообщения с командой /start
    """
    # Метод answer позволяет отправить сообщение в ответ на полученное сообщение
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}!")

# Обработчик для всех остальных сообщений
@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    Обработчик отправит полученное сообщение обратно отправителю

    По умолчанию, обработчик сообщений будет обрабатывать все типы сообщений (текст, фото, стикер и др.)
    """
    try:
        # Отправляем копию полученного сообщения
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # Не все типы сообщений поддерживают копирование, поэтому обрабатываем исключение
        await message.answer("Попробуйте еще раз!")

async def main() -> None:
    # Инициализируем экземпляр бота с указанием режима разбора сообщений (ParseMode)
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # Запускаем обработку событий с использованием Dispatcher
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
