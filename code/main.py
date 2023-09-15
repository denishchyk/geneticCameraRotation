import time
from typing import List

import cv2
import datetime as datetime
import numpy as np
import requests

import Private_setting
import angle_of_rotation
import genetics
import data_storageSQLlite
import tg_bot
from img import save_image


def update_guides(): pass
def one_camera(camera):
    next_generation = []
    api_url = f"http://{Private_setting.ip}/screenshot/{camera.guid}?password={Private_setting.password}"
    print(api_url)
    response = requests.get(api_url, verify=False)
    #TODO response.status_code == 200 как обрабатывать
    camera.status_code = response.status_code == 200
    camera.content_type = camera.status_code and 'image' in response.headers.get('Content-Type')
    if camera.content_type:
        img_data = response.content
        save_image(img_data, "./images/", camera.name )
        image = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_COLOR)
        # TODO модуль ГА переписать
        yang = genetics.STEP1_initialize_population_from_frame(image)

        # TODO модуль детекции переписать
        matches = genetics.STEP2_wedding(camera.old, yang)
        camera.angle = abs(
            angle_of_rotation.calculate_rotation_angle(camera.old, yang, matches)) if camera.keypoint_count > 0 else 0
        camera.turn = camera.angle < Private_setting.threshold
        if camera.turn:
            next_generation = genetics.STEP3_crossover(yang, camera.old, matches) + genetics.STEP4_selection(yang, matches)
            camera.old = [chromosome for chromosome in next_generation if chromosome.fitness > 1]

        else:
            tg_bot.tell_the_bot()
            camera.old = camera.old + yang[:10]
        for i in camera.old:
            i.fitness -= 1
            #i.save_to_database(name)
        camera.keypoint_count = len(camera.old)

    return camera


class Camera:
    def __init__(self,
                 name: str,  # Наименование камеры (строка)
                 guid: str,  # Уникальный идентификатор камеры (строка)
                 datetime: datetime,  # Дата и время записи (объект datetime)
                 old: List[genetics.KC] = [],  # Список ключевых точек (список объектов)
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


cameras = data_storageSQLlite.read_from_database()


flag = False #Флаг проверяет что трассир имеет актуальные гуиды
while True:
    try:
        if flag:
            for i in range(len(cameras)):
                cameras[i] = one_camera(cameras[i])
                if not cameras[i].content_type :
                    flag = False
                    break

            data_storageSQLlite.database_entry(cameras)
            print("все камеры")
            if flag: time.sleep(10)
        else:
            flag = True
            update_guides()
    except Exception as e:
        print(f"Ошибка при обращении к API: {e}")























