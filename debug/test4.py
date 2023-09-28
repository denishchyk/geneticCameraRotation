import cv2
import numpy as np
import requests

import Private_setting

import aiohttp
import asyncio

async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print("response.content",response.content)
            try:
                data = await response.read()
            except aiohttp.ClientPayloadError as e:
                print(f"ClientPayloadError: {e}")
                data = b''  # Пустые данные в случае ошибки
            return data

async def run_requests(url, num_requests):
    tasks = [fetch_url(url) for _ in range(num_requests)]
    responses = await asyncio.gather(*tasks)
    return responses

async def main():
    url = "http://localhost:5000/screenshot/Aqi3PH68?password=masha"
    num_requests_per_thread = 10
    num_threads = 5
    total_requests = num_requests_per_thread * num_threads

    thread_tasks = [run_requests(url, num_requests_per_thread) for _ in range(num_threads)]

    thread_responses = await asyncio.gather(*thread_tasks)

    # Сохраняем бинарные данные изображений в массив
    image_data_array = []
    for responses in thread_responses:
        for response in responses:
            image_data_array.append(response)

    # Теперь image_data_array содержит бинарные данные всех загруженных изображений

if __name__ == "__main__":
    asyncio.run(main())