from typing import List

import cv2
import datetime as datetime
import numpy as np
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, relationship, DeclarativeBase

from Private_setting import bd_name
from code.genetics import KC


# Создаем подключение к базе данных SQLite
engine = create_engine(f'sqlite:///{bd_name}.db')
# Создаем базовый класс для описания моделей
class Base(DeclarativeBase):pass

# Определяем модель данных (таблицу) Camera
class ORM_Camera(Base):

    __tablename__ = 'cameras'


    name = Column(String, primary_key=True)
    guid = Column(String)
    angle = Column(Float)
    datetime = Column(String)  # Подставьте нужный тип данных
    keypoint_count = Column(Integer)
    generations_count = Column(Integer)
    generations_max = Column(Integer)
    # status_code = Column(Integer)
    # content_type = Column(String)  # Подставьте нужный тип данных
    # turn = Column(Integer)
    # Определяем отношение к таблице keypoints

    keypoints = relationship('ORM_Keypoint', back_populates='camera')
    def __init__(self, name, guid, angle, datetime, keypoint_count, generations_count, generations_max):
        self.name = name
        self.guid = guid
        self.angle = angle
        self.datetime = datetime
        self.keypoint_count = keypoint_count
        self.generations_count = generations_count
        self.generations_max = generations_max





# Определяем модель данных (таблицу) Keypoint
class ORM_Keypoint(Base):
    __tablename__ = 'keypoints'

    id = Column(Integer, primary_key=True)
    camera_name = Column(String, ForeignKey('cameras.name'))
    x = Column(Float)
    y = Column(Float)
    size = Column(Float)
    angle = Column(Float)
    response = Column(Float)
    octave = Column(Integer)
    fitness = Column(Float)
    number_of_generations = Column(Integer)
    distance = Column(Float)
    avg_distance = Column(Float)
    step = Column(Integer)
    descriptor = Column(String)

    # Связь с камерой
    camera = relationship('ORM_Camera', back_populates='keypoints')

    def __init__(self, camera_name, x, y, size, angle, response, octave, fitness, number_of_generations, distance,
                 avg_distance, step, descriptor):
        self.camera_name = camera_name
        self.x = x
        self.y = y
        self.size = size
        self.angle = angle
        self.response = response
        self.octave = octave
        self.fitness = fitness
        self.number_of_generations = number_of_generations
        self.distance = distance
        self.avg_distance = avg_distance
        self.step = step
        self.descriptor = descriptor
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

def database_entry(cameras):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:

        # Для каждой камеры в списке
        for camera_data in cameras:
            # Найдем камеру в базе данных по имени
            camera = session.query(ORM_Camera).filter_by(name=camera_data.name).first()

            if camera:
                # Обновляем данные камеры
                camera.angle = camera_data.angle
                camera.datetime = camera_data.datetime
                camera.keypoint_count = camera_data.keypoint_count
                camera.generations_count = camera_data.generations_count
                camera.generations_max = camera_data.generations_max



                # Удаляем старые ключевые точки этой камеры
                session.query(ORM_Keypoint).filter_by(camera_name=camera.name).delete()
                #
                #
                # # # Добавляем новые ключевые точки
                for keypoint_data in camera_data.old:
                    keypoint = ORM_Keypoint(
                                camera_name = camera_data.name,
                                x=keypoint_data.KeyPoint.pt[0],
                                y=keypoint_data.KeyPoint.pt[1],
                                size=keypoint_data.KeyPoint.size,
                                angle=keypoint_data.KeyPoint.angle,
                                response=keypoint_data.KeyPoint.response,
                                octave=keypoint_data.KeyPoint.octave,
                                fitness=keypoint_data.fitness,
                                number_of_generations=keypoint_data.number_of_generations,
                                distance=keypoint_data.distance,
                                avg_distance=keypoint_data.avg_distance,
                                step=keypoint_data.step,
                                descriptor=keypoint_data.descriptor
                            )
                    session.add(keypoint)

        # Фиксируем изменения в базе данных
        session.commit()
    except Exception as e:
        # Если произошла ошибка, откатываем транзакцию
        session.rollback()
        print(f"Ошибка при обновлении базы данных: {e}")
    finally:
        # Закрываем сессию
        session.close()


# Функция для считывания всех камер и их ключевых точек
def read_from_database():

    Session = sessionmaker(bind=engine)
    session = Session()

    # Получить все записи из таблицы ORM_Camera
    camera_records = session.query(ORM_Camera).all()
    cameras = []
    for camera_record in camera_records:
        camera = Camera(
            name=camera_record.name,
            guid=camera_record.guid,
            datetime=camera_record.datetime,
            angle=camera_record.angle,
            keypoint_count=camera_record.keypoint_count,
            generations_count=camera_record.generations_count,
            generations_max=camera_record.generations_max
        )
        # Добавить созданный объект Camera в список cameras
        cameras.append(camera)

    # Для каждой камеры считываем соответствующие ключевые точки
    for camera in cameras:
        keypoints = session.query(ORM_Keypoint).filter_by(camera_name=camera.name).all()
        for keypoint in keypoints:
            descriptor = np.frombuffer(keypoint.descriptor, dtype=np.float32)
            camera.old.append(KC(
                KeyPoint=cv2.KeyPoint(keypoint.x, keypoint.y, keypoint.size, keypoint.angle, keypoint.response,
                                      keypoint.octave, keypoint.id),
                descriptor=descriptor,
                fitness=keypoint.fitness,
                number_of_generations=keypoint.number_of_generations,
                distance=keypoint.distance,
                avg_distance=keypoint.avg_distance,
                step=keypoint.step
            ))

    session.close()

    return cameras

def update_guides_in_bd(guids_dict):
    # Инициализируем соединение с базой данных и создаем сессию
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        for i in guids_dict:
            name, guid = next(iter(i.items()))
            # Проверяем, существует ли камера с таким именем
            existing_camera = session.query(ORM_Camera).filter_by(name=name).first()

            if existing_camera:
                # Если камера с таким именем уже существует, обновляем GUID
                existing_camera.guid = guid
            else:
                # Если камера с таким именем не существует, создаем новую камеру
                new_camera = ORM_Camera(name=name, guid=guid)
                session.add(new_camera)

        # Фиксируем изменения в базе данных
        session.commit()
    except Exception as e:
        # Если произошла ошибка, откатываем транзакцию
        session.rollback()
        print(f"Ошибка при обновлении/добавлении камер: {e}")
    finally:
        # Закрываем сессию
        session.close()

# Функция для создания таблиц в базе данных
def create_tables():
    Base.metadata.create_all(engine)

# Функция для добавления начальных данных (первичное заполнение)
def add_initial_data(cameras):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        for camera_data in cameras:
            camera = ORM_Camera(
                name=camera_data.name,
                guid=camera_data.guid,
                angle=camera_data.angle,
                datetime=camera_data.datetime,
                keypoint_count=camera_data.keypoint_count,
                generations_count=camera_data.generations_count,
                generations_max=camera_data.generations_max
            )
            session.add(camera)
            session.flush()


            for keypoint_data in camera_data.old:
                # TODO сделать орм и объект сопостовляемыми
                # keypoint = ORM_Keypoint(**keypoint_data)
                # keypoint.camera = camera
                keypoint = ORM_Keypoint(
                                camera_name = camera_data.name,
                                x=keypoint_data.KeyPoint.pt[0],
                                y=keypoint_data.KeyPoint.pt[1],
                                size=keypoint_data.KeyPoint.size,
                                angle=keypoint_data.KeyPoint.angle,
                                response=keypoint_data.KeyPoint.response,
                                octave=keypoint_data.KeyPoint.octave,
                                fitness=keypoint_data.fitness,
                                number_of_generations=keypoint_data.number_of_generations,
                                distance=keypoint_data.distance,
                                avg_distance=keypoint_data.avg_distance,
                                step=keypoint_data.step,
                                descriptor=keypoint_data.descriptor
                            )

                session.add(keypoint)

        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Ошибка при записи в базу данных: {e}")
    finally:
        session.close()