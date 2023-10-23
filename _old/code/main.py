import time

import Private_setting
from code.rotate import genetics, angle_of_rotation
import data_storageSQLlite
import tg_bot
from code.trassir import get_img
from img import save_image, img_to_frame

def update_guides(): pass

def one_camera(camera):
    f,img = get_img(camera.guid)
    if f and img:
        save_image(img, "./images/", camera.name )
        yang = genetics.STEP1_initialize_population_from_frame(img_to_frame(img))

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


cameras = data_storageSQLlite.read_from_database()


flag = False #Флаг проверяет что трассир имеет актуальные гуиды
while True:
    try:
        if flag:
            for i in range(len(cameras)):
                cameras[i] = one_camera(cameras[i])
                if not cameras[i].content_type:
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























