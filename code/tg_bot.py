from Private_setting import chat_id_masha
CHAT_ID = chat_id_masha
DB_FILE = 'it_could_be_MySQL.db'

import asyncio
import logging
from datetime import datetime, timedelta
import sqlite3

from aiogram import Bot, Dispatcher, types, html, F


from config_reader import config

bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

def get_recent_events():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Вычисляем время, за которое нужно получить события
    now = datetime.now()
    five_minutes_ago = now - timedelta(minutes=15)
    # Запрос к базе данных для получения событий за последние 5 минут
    cursor.execute('SELECT name, datetime FROM event WHERE datetime >= ?', (five_minutes_ago,))
    recent_events = cursor.fetchall()

    conn.close()
    return recent_events
@dp.message(F.text)
async def echo_with_time(message: types.Message):
    # Получаем текущее время в часовом поясе ПК
    time_now = datetime.now().strftime('%H:%M')
    # Создаём подчёркнутый текст
    added_text = html.underline(f"Создано в {time_now}")
    # Отправляем новое сообщение с добавленным текстом
    await message.answer(f"{message.html_text}\n\n{added_text}")


# Function to send the current time
async def send_current_time():
    while True:
        try:
            # Получаем последние события
            recent_events = get_recent_events()
            message = ""
            for event in recent_events:
                event_name, event_datetime = event
                message += f"Событие: {event_name}\tВремя: {event_datetime}\n"

            await bot.send_message(chat_id=CHAT_ID, text=message)

            await asyncio.sleep(10)  # Send the time every minute
        except Exception as e:
            logging.error(str(e))



async def main():
    # Start the message sending task
    asyncio.create_task(send_current_time())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
