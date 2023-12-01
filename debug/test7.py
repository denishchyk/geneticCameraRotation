import asyncio
import threading

import aiohttp
import os
from datetime import datetime, timedelta

# URL для скачивания
url = "https://w.forfun.com/fetch/fa/fa42c1c2a72af7fad3f7b1edb0d09721.jpeg"

# Список имен для запросов
names = [f"Камера_{i}" for i in range(52)]

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
                filename = os.path.join(image_folder, f"{name} datetime {current_time}.jpg")
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
    print("cleanup")
    for filename in os.listdir(image_folder):

        file_path = os.path.join(image_folder, filename)  # Получаем полный путь к файлу

        try:
            # Получаем дату и время из названия файла
            name, file_time = filename.rsplit('datetime ', 1)
            file_time = datetime.strptime(file_time, "%Y-%m-%d_%H-%M-%S.jpg")

            # Если файл старше 15 минут, удаляем его
            if current_time - file_time > timedelta(seconds=20):
                os.remove(file_path)
                print(f"Удалено устаревшее изображение: {filename}")
        except ValueError as e:
            print(e)
            pass  # Пропускаем файлы с неверным форматом имени
    return None


# Запускаем асинхронные задачи скачивания


async def download_images(queue):
    """
    Асинхронно загружает изображения из очереди.

    Аргументы:
    queue: asyncio.Queue - очередь с именами изображений для загрузки.

    Возвращает:
    downloaded_images: list - список скачанных изображений.

    Эта функция инициирует сеанс aiohttp и циклически извлекает имена изображений из очереди,
    выполняя асинхронные запросы на скачивание каждого изображения.
    Имя каждого успешно скачанного файла добавляется в список 'downloaded_images'.
    После обработки каждого элемента в очереди функция отправляет сигнал о завершении задачи.

    """
    async with aiohttp.ClientSession() as session:
        downloaded_images = []  # Массив для хранения имен скачанных изображений

        # Пока очередь не пуста, извлекаем элементы из очереди
        while not queue.empty():
            name = await queue.get()
            # Вызываем функцию для скачивания изображения и получаем имя файла
            filename = await download_image(session, name)
            if filename:
                # Добавляем имя файла в массив скачанных изображений
                downloaded_images.append(filename)
            queue.task_done()
        # Возвращаем массив скачанных изображений
        return downloaded_images


# Основная асинхронная функция для скачивания изображений
async def main():
    # Создаем очередь для хранения имен файлов
    while 1:
        queue = asyncio.Queue()

        # Заполняем очередь именами из списка names
        for i in range(len(names)//max_concurrent_downloads):
            for name in names[i * 5 : (i + 1) * 5]:
                queue.put_nowait(name)

            tasks = []
            # Запускаем несколько задач для асинхронного скачивания изображений
            task = asyncio.create_task(download_images(queue))
            tasks.append(task)

            # Ожидаем завершения всех задач
            await asyncio.gather(*tasks)
            await queue.join()

        ostatok = len(names)%max_concurrent_downloads
        if ostatok:
            for name in names[-ostatok:]:
                queue.put_nowait(name)

            tasks = []
            # Запускаем несколько задач для асинхронного скачивания изображений
            task = asyncio.create_task(download_images(queue))
            tasks.append(task)

            # Ожидаем завершения всех задач
            await asyncio.gather(*tasks)
            await queue.join()

        # Выполняем очистку директории с изображениями от устаревших файлов
        cleanup_image_folder()

if __name__ == '__main__':
    # Создаем цикл событий asyncio
    loop = asyncio.get_event_loop()

    # Запускаем основную асинхронную функцию
    loop.run_until_complete(main())