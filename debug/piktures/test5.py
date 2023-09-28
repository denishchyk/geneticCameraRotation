from multiprocessing.dummy import Pool as ThreadPool
import itertools
import requests
import threading
import concurrent.futures

# Define the URL and names for the requests
url = "http://localhost:5000/screenshot/AIhKLrez?password=masha"  # Replace with your target URL
names = [f"Камера {i}" for i in range(55)]  # Replace with your request names
# Максимальное количество одновременных загрузок
max_concurrent_downloads = 5
# Тайм-аут для запросов (в секундах)
request_timeout = 150  # Установите значение, подходящее для вашего случая


import asyncio
import aiohttp


# Функция для скачивания изображения по URL с использованием aiohttp
async def download_image(session, name):
    try:
        async with  session.get(url, timeout=request_timeout) as response:
            if response.status == 200:
                image_data = await response.read()
                filename = f"./piktures/pi{name}.jpg"
                with open(filename, "wb") as f:
                    f.write(image_data)
                print(f"Скачано: {name} {filename}")
            else:
                print(f"Ошибка при скачивании изображения {url}: {response.status}")
    except Exception as e:
        print(f"Ошибка при скачивании изображения {url}: {str(e)}")

# Запускаем асинхронные задачи скачивания
async def download_images(queue):
    async with aiohttp.ClientSession() as session:
        while not queue.empty():
            url = await queue.get()
            await download_image(session, url)
            queue.task_done()




# Запускаем асинхронные задачи скачивания
async def main():
    queue = asyncio.Queue()

    for name in names:
        queue.put_nowait(name)

    tasks = []
    for _ in range(max_concurrent_downloads):
        task = asyncio.create_task(download_images(queue))
        tasks.append(task)

    await asyncio.gather(*tasks)
    await queue.join()

# Запускаем основной цикл asyncio
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

# Теперь все 200 изображений скачаны


# В этой точке все запросы завершены

# def send_post_request(url, name):
#     response = requests.get(url, data={"name": name})
#     return response
#
# with ThreadPool(len(names)) as pool:
#     # Use starmap to send POST requests with different names
#     res = pool.starmap(send_post_request, zip(itertools.repeat(url), names))
#
# # Now, the 'res' list contains the responses for each request
# for i, response in enumerate(res):
#     print(f"Response for {names[i]}: {len(response.content),type(response.content)}")
