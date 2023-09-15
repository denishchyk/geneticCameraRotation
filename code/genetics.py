
import cv2
import numpy as np
import random
import sqlite3




class KC:
    # KeypointChromosome

    """
cv.KeyPoint(x=100, y=50, _size=10, _angle=45, _response=0.8, _octave=2)
    pt: Координаты ключевой точки в формате tuple(x, y).
    size: Размер ключевой точки.
    angle: Угол ключевой точки.
    response: Отклик (значение ответа) ключевой точки.
    octave: Октава, к которой принадлежит ключевая точка.
    class_id: Идентификатор класса (некоторые версии OpenCV могут иметь это поле).

my_database.db keypoints
    1   camera_id
        KeyPoint
    2       id : class_id
    3       x  : pt[0]
    4       y  : pt[1]
    5       size
    6       angle
    7       response
    8       octave
    9   descriptor,
    10  fitness
    11  number_of_generations
    12  distance
    13  avg_distance
    14  global_step
    """

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


    def save_to_database(self, db_path='my_database.db'):
        # Устанавливаем соединение с базой данных
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Вставляем данные текущего объекта KeypointChromosome в таблицу keypoints
        cursor.execute(
            '''
                INSERT INTO keypoints (
                    id,
                    x ,
                    y,
                    size,
                    angle,
                    response,
                    octave,
                    descriptor,
                    fitness,
                    number_of_generations,
                    distance,
                    avg_distance,
                    step

                )
                VALUES (?, ?, ?,?, ?, ?,?, ?, ?,?, ?, ?,?)
            ''',
            (
                self.KeyPoint.class_id,
                self.KeyPoint.pt[0],
                self.KeyPoint.pt[1],
                self.KeyPoint.size,
                self.KeyPoint.angle,
                self.KeyPoint.response,
                self.KeyPoint.octave,
                self.descriptor,
                self.fitness,
                self.number_of_generations,
                self.distance,
                self.avg_distance,
                self.step,
            )
         )

        # Сохраняем изменения в базе данных
        # Закрываем соединение с базой данных
        conn.commit()
        conn.close()

    def save_to_db(self, db_path='my_database.db'):
        # Устанавливаем соединение с базой данных
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Вставляем данные текущего объекта KeypointChromosome в таблицу keypoints
        cursor.execute('''
                    INSERT INTO keypoints2 (
                        id,
                        fitness,
                        number_of_generations,
                        distance,
                        avg_distance,
                        step

                    )
                    VALUES (?, ?, ?,?, ?, ?)
                ''', (
            self.KeyPoint.class_id,
            self.fitness,
            self.number_of_generations,
            self.distance,
            self.avg_distance,
            self.step,
        )
                       )

        # Сохраняем изменения в базе данных
        # Закрываем соединение с базой данных
        conn.commit()
        conn.close()


def STEP1_initialize_population_from_frame(frame):
    """
    Инициализирует начальную популяцию хромосом ключевых точек на основе кадра видео.
    инициализируем только 2 обязательных параметра cv.KeyPoint и дискриптор

    Аргументы:
    - frame: Исходный кадр видео.

    Возвращает:
    - population: Список объектов KeypointChromosome, представляющих начальную популяцию ключевых точек.
    """

    # Преобразование кадра в оттенки серого
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Создание детектора ORBр
    orb = cv2.ORB_create()

    # Обнаружение ключевых точек и вычисление дескрипторов
    keypoints, descriptors = orb.detectAndCompute(frame_gray, None)

    # Преобразование дескрипторов в формат float32
    d = descriptors.astype(np.float32)

    # Инициализация популяции
    population = []
    for i, keypoint in enumerate(keypoints):
        # Создание хромосомы для ключевой точки
        chromosome = KC(keypoint, d[i])
        population.append(chromosome)

    return population


def STEP2_wedding(old, yang):
    # Выполнение матчинга дескрипторов между текущим и предыдущим поколениями
    # Извлечение дескрипторов из предыдущего и текущего поколений
    descriptors_yang = np.array([ch.descriptor for ch in yang])
    descriptors_old = np.array([ch.descriptor for ch in old])

    # Создание объекта matcher
    bf = cv2.FlannBasedMatcher()
    return bf.knnMatch(descriptors_old, descriptors_yang, k=1)  # Вычисление всех матчей

def STEP3_crossover(yang, old, matches):
    global global_c
    selected_matches = [match for match in matches if
                        match[0].distance <= global_c]  # Фильтрация матчей с расстоянием менее

    # Создание массива партнеров для скрещивания и заполнение -1, размерность = размерности previous_generation
    partners = [(-1, float("inf"))] * len(old)
    # Присваивание партнеров для скрещивания
    for match in selected_matches:
        if match[0].distance < partners[match[0].queryIdx][1]:
            partners[match[0].queryIdx] = (match[0].trainIdx, match[0].distance)

    for i, (j, d) in enumerate(partners):
        if j > -1:
            if not old[i].distance:
                old[i].avg_distance = d
            old[i].fitness += 10 / (d + 1)
            old[i].distance = d
            old[i].avg_distance = (old[i].avg_distance * old[i].number_of_generations + d) / (
                        old[i].number_of_generations + 1)
            old[i].number_of_generations += 1

            if random.randint(0, 1):
                id = old[i].KeyPoint.class_id
                old[i].KeyPoint = yang[j].KeyPoint
                old[i].KeyPoint.class_id = id

    # Сортируем массив по значению fitness в убывающем порядке
    old_thoroughbred = sorted(old, key=lambda x: x.number_of_generations, reverse=True)
    for x in old_thoroughbred[:30]: x.fitness += 1

    old = sorted(old_thoroughbred[30:], key=lambda x: x.fitness, reverse=True)

    old_mutants = old[400:]
    random.shuffle(old_mutants)

    return old[:400] + old_thoroughbred[:30] + old_mutants[:50]

def STEP4_selection(yang, matches):
    global global_m
    new_yang = []
    matches_train_idx = set(
        [match[0].trainIdx for match in matches] +
        [match[0].trainIdx for match in matches if match[0].distance > global_m]
    )
    for i, y in enumerate(yang):
        if i not in matches_train_idx:
            y.set_id()
            new_yang.append(y)

    random.shuffle(new_yang)
    return new_yang[:50]