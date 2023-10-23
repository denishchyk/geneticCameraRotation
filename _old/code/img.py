import os

import cv2
import numpy as np


def save_image(image_data, directory, filename):
    """
    Сохраняет изображение в указанную директорию с указанным именем файла.

    :param image_data: Данные изображения в виде байтов
    :param directory: Путь к директории, в которую нужно сохранить изображение
    :param filename: Имя файла для сохранения
    :return: Путь к сохраненному изображению или None в случае ошибки
    """
    try:
        # Проверяем, существует ли директория, и создаем ее, если не существует
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Создаем полный путь к файлу
        file_path = os.path.join(directory, filename + "jpg")

        # Открываем файл для записи бинарных данных
        with open(file_path, 'wb') as file:
            file.write(image_data)

    except Exception as e:
        print(f"Ошибка при сохранении изображения: {e}")

def img_to_frame(img):
    return  cv2.imdecode(np.frombuffer(img, np.uint8), cv2.IMREAD_COLOR)