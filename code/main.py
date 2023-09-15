import time
import cv2
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
                 name, guid,  datetime,
                 angle = 0,
                 keypoint_count = 0, generations_count = 0, generations_max = 0,
                 old = []
                 ):
        self.name = name
        self.guid = guid
        self.angle = angle
        self.datetime = datetime
        self.keypoint_count = keypoint_count
        self.generations_count = generations_count
        self.generations_max = generations_max
        self.old = old  # Массив ключевых точек по ключу из другой таблицы
        self.status_code = True
        self.content_type = True
        self.turn = True

cameras = data_storage.read_from_database()


flag = False #Флаг проверяет что трассир имеет актуальные гуиды
while True:
    try:
        if flag:
            for i in range(len(cameras)):
                cameras[i] = one_camera(cameras[i])
                if not cameras[i].content_type :
                    flag = False
                    break

            data_storage.database_entry(cameras)
            print("все камеры")
            if flag: time.sleep(10)
        else:
            flag = True
            update_guides()
    except Exception as e:
        print(f"Ошибка при обращении к API: {e}")























