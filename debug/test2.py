import concurrent.futures
import random
import time

import cv2
import numpy as np
import requests

import Private_setting
def img_to_frame(img):
    return  cv2.imdecode(np.frombuffer(img, np.uint8), cv2.IMREAD_COLOR)
def get_img(camera):
    api_url = f"http://{Private_setting.ip}/screenshot/{camera}?password={Private_setting.password}"
    max_retries = 3  # Количество попыток
    for _ in range(max_retries):
        try:
            response = requests.get(api_url, timeout=30)
            response.raise_for_status()
            if 'image' in response.headers.get('Content-Type') :
                print(f"опытка номер {_}\t ")
                return True, response.content
            else:
                print(f"return True, False")
                return True, False
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе изображения для камеры {_}: {str(e)}")

    # Если не удалось получить изображение после множества попыток, верните False
    print(f"требовалось больше чем {max_retries}\t ")
    return False, False

# Функция для обновления данных для группы камер
def update_camera_data(camera_group):
    results = []
    for camera in camera_group:
        # Ваш код обновления данных для камеры
        flag ,img = get_img("AIhKLrez")
        print(camera,flag ,img[-10:], len(img))
        frame = img_to_frame(img)
        print("\timg\t", type(frame))
        imgcv2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        time.sleep(random.uniform(0.4, 0.01))
        result = f"Обновление данных для камеры {camera}"
        results.append(imgcv2)
    return results

# Создаем список камер
all_cameras = [f"Камера {i}" for i in range(6, 50)]

# Разбиваем камеры на группы по 10
camera_groups = [all_cameras[i:i+10] for i in range(0, len(all_cameras), 10)]

# Определяем оставшиеся камеры
remaining_cameras = all_cameras[len(camera_groups) * 10:]

# Создаем ThreadPoolExecutor с пятью потоками
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    all_results = []

    # Запускаем потоки для каждой группы камер
    for camera_group in camera_groups:
        future = executor.submit(update_camera_data, camera_group)
        all_results.append(future)

    # Запускаем потоки для оставшихся камер
    if remaining_cameras:
        future = executor.submit(update_camera_data, remaining_cameras)
        all_results.append(future)

    # Ждем завершения всех потоков и получаем результаты
    combined_results = []
    for future in concurrent.futures.as_completed(all_results):
        combined_results.extend(future.result())

# Теперь combined_results содержит результаты всех потоков
print(combined_results)

