import asyncio
import aiohttp
import os
from datetime import datetime, timedelta

# URL для скачивания
url = "https://w.forfun.com/fetch/fa/fa42c1c2a72af7fad3f7b1edb0d09721.jpeg"

# Список имен для запросов
names = [f"Камера {i}" for i in range(200)]

# Максимальное количество одновременных загрузок
max_concurrent_downloads = 5

# Тайм-аут для запросов (в секундах)
request_timeout = 150

# Папка для сохранения изображений
image_folder = "./piktures"

# Создание папки для сохранения изображений, если она не существует
if not os.path.exists(image_folder):
    os.makedirs(image_folder)


# Функция для скачивания изображения по URL с использованием aiohttp
async def download_image(session, name):
    try:
        async with session.get(url, timeout=request_timeout) as response:
            if response.status == 200:
                image_data = await response.read()
                # Генерируем имя файла с именем и текущей датой и временем
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = os.path.join(image_folder, f"{name}_{current_time}.jpg")
                with open(filename, "wb") as f:
                    f.write(image_data)
                print(f"Скачано: {name} {filename}")
                return filename  # Возвращаем имя скачанного файла
            else:
                print(f"Ошибка при скачивании изображения {url}: {response.status}")
                return None
    except Exception as e:
        print(f"Ошибка при скачивании изображения {url}: {str(e)}")
        return None


# Функция для очистки директории от устаревших изображений
def cleanup_image_folder():
    current_time = datetime.now()
    for filename in os.listdir(image_folder):
        file_path = os.path.join(image_folder, filename)
        try:
            # Получаем дату и время из названия файла
            name, file_time = filename.rsplit('_', 1)
            file_time = datetime.strptime(file_time, "%Y-%m-%d_%H-%M-%S.jpg")
            # Если файл старше 15 минут, удаляем его
            if current_time - file_time > timedelta(minutes=15):
                os.remove(file_path)
                print(f"Удалено устаревшее изображение: {filename}")
        except ValueError:
            pass  # Пропускаем файлы с неверным форматом имени


# Запускаем асинхронные задачи скачивания
async def download_images(queue):
    async with aiohttp.ClientSession() as session:
        downloaded_images = []  # Массив для хранения имен скачанных изображений
        while not queue.empty():
            name = await queue.get()
            filename = await download_image(session, name)
            if filename:
                downloaded_images.append(filename)
            queue.task_done()
        return downloaded_images  # Возвращаем массив скачанных изображений


# Запускаем основную асинхронную функцию
async def main():
    queue = asyncio.Queue()

    # Заполняем очередь именами из списка names
    for name in names:
        queue.put_nowait(name)

    tasks = []
    for _ in range(max_concurrent_downloads):
        task = asyncio.create_task(download_images(queue))
        tasks.append(task)

    # Ожидаем завершения всех задач
    await asyncio.gather(*tasks)
    await queue.join()


if __name__ == '__main__':
    # Запускаем асинхронную функцию для скачивания
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    # Очищаем директорию от устаревших изображений
    cleanup_image_folder()
