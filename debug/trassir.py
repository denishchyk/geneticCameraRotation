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


def get_img(guid):
    api_url = f"http://{Private_setting.ip}/screenshot/{guid}?password={Private_setting.password}"
    print(api_url)
    response = requests.get(api_url, verify=False)
    # TODO response.status_code == 200 как обрабатывать
    if response.status_code == 200:
        if 'image' in response.headers.get('Content-Type'):
             return True,response.content
        else: return True, False
    else:
        return False, False