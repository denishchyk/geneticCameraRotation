import asyncio
import aiohttp
import os
from datetime import datetime, timedelta
import threading

# URL для скачивания
url = "https://w.forfun.com/fetch/fa/fa42c1c2a72af7fad3f7b1edb0d09721.jpeg"

# Папка для сохранения изображений
image_folder = "./piktures"

# Создание папки для сохранения изображений, если она не существует
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

# Функция для скачивания изображения по URL с использованием aiohttp
async def download_image(session):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                image_data = await response.read()
                # Генерируем имя файла с текущей датой и временем
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = os.path.join(image_folder, f"{current_time}.jpg")
                with open(filename, "wb") as f:
                    f.write(image_data)
                print(f"Скачано: {filename}")
            else:
                print(f"Ошибка при скачивании изображения {url}: {response.status}")
    except Exception as e:
        print(f"Ошибка при скачивании изображения {url}: {str(e)}")

# Функция для удаления устаревших изображений
def cleanup_image_folder():
    while True:
        current_time = datetime.now()
        for filename in os.listdir(image_folder):
            file_path = os.path.join(image_folder, filename)
            try:
                # Получаем дату и время из названия файла
                name, file_time = filename.rsplit('_', 1)
                file_time = datetime.strptime(filename, "%Y-%m-%d_%H-%M-%S.jpg")
                # Если файл старше 15 минут, удаляем его
                if current_time - file_time > timedelta(minutes=2):
                    os.remove(file_path)
                    print(f"Удалено устаревшее изображение:{filename}")
            except ValueError:
                pass  # Пропускаем файлы с неверным форматом имени

# Запускаем асинхронный цикл для скачивания изображений
async def main():
    while True:
        async with aiohttp.ClientSession() as session:
            await download_image(session)
            await asyncio.sleep(1)  # Подождать 1 секунду между скачиваниями

if __name__ == '__main__':
    # Запускаем бесконечный цикл скачивания и удаления изображений в отдельном потоке
    cleanup_thread = threading.Thread(target=cleanup_image_folder)
    cleanup_thread.daemon = True
    cleanup_thread.start()

    # Запускаем асинхронный цикл для скачивания изображений
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
