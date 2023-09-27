import cv2
import numpy as np
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import sessionmaker, relationship, DeclarativeBase

from Private_setting import bd_name



# Создаем подключение к базе данных SQLite
engine = create_engine(f'sqlite:///{bd_name}.db')
# Создаем базовый класс для описания моделей
# class Base(DeclarativeBase):pass
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class ORM_Statys(Base):
    __tablename__ = 'statys'
    name = Column(String, primary_key=True)
    flag = Column(Integer)
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

# Определите модель для таблицы "event"
class ORM_Event(Base):
    __tablename__ = 'event'
    event_pk = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    datetime = Column(DateTime)
    enabled = Column(Integer)
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



def read_from_database():

    Session = sessionmaker(bind=engine)
    session = Session()

    # Получить все записи из таблицы ORM_Camera
    camera_records = session.query(ORM_Camera).all()
    cameras = []
    for camera_record in camera_records:
        from debug.camera_keypoint import Camera
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
            from debug.camera_keypoint import KC
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