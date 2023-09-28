import json
from typing import List

from datetime import datetime

import requests

import Private_setting
from code.rotate.genetics import KC


class Camera:
    def __init__(self,
                 name: str,  # Наименование камеры (строка)
                 guid: str,  # Уникальный идентификатор камеры (строка)
                 datetime: datetime,  # Дата и время записи (объект datetime)
                 old: List[KC] = [],  # Список ключевых точек (список объектов)
                 angle: float = 0.0,  # Угол камеры (число с плавающей точкой)
                 keypoint_count: int = 0,  # Количество ключевых точек (целое число)
                 generations_count: int = 0,  # Количество поколений (целое число)
                 generations_max: int = 0,  # Максимальное количество поколений (целое число)

                 status_code: bool = True,  # Код состояния (True - 200, False - != 200)
                 content_type: bool = True,  # Тип контента (True - изображение, False - не изображение)
                 turn: bool = True  # Статус включения (True - статичное состояние, False - поворот)
                 ):

        """
        Класс представляет камеру и её характеристики.

        :param name: Наименование камеры.
        :param guid: Уникальный идентификатор камеры.
        :param datetime: Дата и время записи.
        :param angle: Угол камеры (по умолчанию 0.0).
        :param keypoint_count: Количество ключевых точек (по умолчанию 0).
        :param generations_count: Количество поколений (по умолчанию 0).
        :param generations_max: Максимальное количество поколений (по умолчанию 0).
        :param old: Список ключевых точек (по умолчанию пустой список).
                    Объект клюжчевая точка хранится в отдельной таблице в базе данных
                    и соединяется по ключу, которым является имя камеры.
        :param status_code: Код состояния (по умолчанию True - активно).
        :param content_type: Тип контента (по умолчанию True - изображение).
        :param turn: Статус включения (по умолчанию True - включено).
        """

        self.name = name
        self.guid = guid
        self.angle = angle
        self.datetime = datetime
        self.keypoint_count = keypoint_count
        self.generations_count = generations_count
        self.generations_max = generations_max
        self.old = old
        self.status_code = status_code
        self.content_type = content_type
        self.turn = turn


def get_guid():
    guid_url = f"http://{Private_setting.ip}/objects/?password={Private_setting.password}"
    response = requests.get(guid_url, verify=False)
    return json.loads(response.content)


# def get_img(guid):
#     api_url = f"http://{Private_setting.ip}/screenshot/{guid}?password={Private_setting.password}"
#     print(api_url)
#     try:
#         response = requests.get(api_url, stream=True, verify=False)
#         # TODO response.status_code == 200 как обрабатывать
#         if response.status_code == 200:
#             if 'image' in response.headers.get('Content-Type'):
#                 # Считываем данные по частям и сохраняем их в буфер
#                 img_data = b""
#                 for chunk in response.iter_content(chunk_size=1024):
#                     img_data += chunk
#                 return True, img_data
#             else:
#                 return True, False
#         else:
#             return False, False
#     except Exception as e:
#         print(f"\tОшибка при получении изображения: {str(e)}")
#         return False, False


from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Создаем сессию с настройками повторных попыток

# Функция для получения изображения с настройками повторных попыток
def get_img(camera):
    api_url = f"http://{Private_setting.ip}/screenshot/{camera}?password={Private_setting.password}"
    max_retries = 3  # Количество попыток
    for _ in range(max_retries):
        try:
            response = requests.get(api_url, timeout=30)
            response.raise_for_status()
            if 'image' in response.headers.get('Content-Type'):
                print(f"опытка номер {_}\t ")
                return True, response.content
            else:
                print(f"return True, False")
                return True, False
        except requests.exceptions.RequestException as e: pass
            # print(f"Ошибка при запросе изображения для камеры {_}: {str(e)}")

    # Если не удалось получить изображение после множества попыток, верните False
    print(f"требовалось больше чем {max_retries}\t ")
    return False, False


