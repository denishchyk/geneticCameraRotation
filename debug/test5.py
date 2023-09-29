import os
import aiohttp
import asyncio
import time

url = "https://w.forfun.com/fetch/fa/fa42c1c2a72af7fad3f7b1edb0d09721.jpeg"
names = [f"Камера {i}" for i in range(200)]

# Максимальное количество одновременных загрузок.
max_concurrent_downloads = 5
# Тайм-аут для запросов (в секундах). Установите значение, подходящее для вашего случая.
request_timeout = 50

# Создание папки для сохранения изображений
if not os.path.exists("./piktures"):
    os.makedirs("./piktures")
# Глобальная переменная для хранения результатов
downloaded_images = []


# Функция для скачивания изображения по URL с использованием aiohttp
async def download_image(session, name):
    try:
        async with session.get(url, timeout=request_timeout) as response:
            if response.status == 200:
                image_data = await response.read()
                filename = f"./piktures/pi{name}.jpg"
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

# Запускаем асинхронные задачи скачивания
async def download_images(queue):
    async with aiohttp.ClientSession() as session:
        while not queue.empty():
            name = await queue.get()
            filename = await download_image(session, name)
            if filename:
                downloaded_images.append(filename)
            queue.task_done()

        #return downloaded_images  # Возвращаем массив скачанных изображений



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


# Запускаем основной цикл asyncio.
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    start_time = time.time()
    loop.run_until_complete(main())

    end_time = time.time()  # Запоминаем время окончания выполнения цикла
    # Вычисляем разницу во времени
    execution_time = end_time - start_time
    print("Все скачанные изображения:", downloaded_images)
    print(f"Время выполнения цикла: {execution_time:.2f} секунд")