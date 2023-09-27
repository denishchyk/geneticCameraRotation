import datetime as datetime
from typing import List


class KC:

    def __init__(self, KeyPoint, descriptor,
                 fitness=10,
                 number_of_generations=1,
                 distance=None, avg_distance=None,
                 step=None
                 ):
        self.KeyPoint = KeyPoint  # cv.KeyPoint
        self.descriptor = descriptor  # Дескриптор точки

        self.fitness = fitness  # Адаптивность точки (по умолчанию равна 10)
        self.number_of_generations = number_of_generations  # Количество поколений
        self.distance = distance  # Расстояние до пары
        self.avg_distance = avg_distance  # avg Расстояние до пары
        self.step = step  # Какой сейчас шаг


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