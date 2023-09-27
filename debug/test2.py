import concurrent.futures
import random
import time

# Функция для обновления данных для группы камер
def update_camera_data(camera_group):
    results = []
    for camera in camera_group:
        # Ваш код обновления данных для камеры
        print(f"Обновление данных для камеры {camera}")
        time.sleep(random.uniform(0.4, 0.01))
        result = f"Обновление данных для камеры {camera}"
        results.append(result)
    return results

# Создаем список камер
all_cameras = [f"Камера {i}" for i in range(6, 227)]

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

