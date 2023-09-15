from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from Private_setting import bd_name

# Создаем подключение к базе данных SQLite
engine = create_engine(f'sqlite:///{bd_name}.db')
# Создаем базовый класс для описания моделей
Base = declarative_base()

# Определяем модель данных (таблицу) Camera
class Camera(Base):
    _tablename__ = 'cameras'


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

    # Связь с ключевыми точками
    keypoints = relationship('Keypoint', back_populates='camera')

# Определяем модель данных (таблицу) Keypoint
class Keypoint(Base):
    __tablename__ = 'keypoints'

    id = Column(Integer, primary_key=True)
    camera_name = Column(Integer, ForeignKey('cameras.name'))
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
    camera = relationship('Camera', back_populates='keypoints')

def database_entry(cameras):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Для каждой камеры в списке
        for camera_data in cameras:
            # Найдем камеру в базе данных по имени
            camera = session.query(Camera).filter_by(name=camera_data['name']).first()

            if camera:
                # Обновляем данные камеры
                camera.angle = camera_data['angle']
                camera.datetime = camera_data['datetime']
                camera.keypoint_count = camera_data['keypoint_count']
                camera.generations_count = camera_data['generations_count']
                camera.generations_max = camera_data['generations_max']

                # Удаляем старые ключевые точки этой камеры
                session.query(Keypoint).filter_by(camera_name=camera.name).delete()

                # Добавляем новые ключевые точки
                for keypoint_data in camera_data['keypoints']:
                    keypoint = Keypoint(**keypoint_data)
                    keypoint.camera = camera
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

    # Считываем все камеры в базе данных
    cameras = session.query(Camera).all()

    # Для каждой камеры считываем соответствующие ключевые точки
    for camera in cameras:
        keypoints = session.query(Keypoint).filter_by(camera_name=camera.name).all()
        camera.old = keypoints

    session.close()

    return cameras

def update_guides_in_bd(guids_dict):
    # Инициализируем соединение с базой данных и создаем сессию
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        for name, guid in guids_dict.items():
            # Проверяем, существует ли камера с таким именем
            existing_camera = session.query(Camera).filter_by(name=name).first()

            if existing_camera:
                # Если камера с таким именем уже существует, обновляем GUID
                existing_camera.guid = guid
            else:
                # Если камера с таким именем не существует, создаем новую камеру
                new_camera = Camera(name=name, guid=guid)
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
            camera = Camera(name=camera_data['name'],
                            guid=camera_data['guid'],
                            angle=camera_data['angle'],
                            datetime=camera_data['datetime'],
                            keypoint_count=camera_data['keypoint_count'],
                            generations_count=camera_data['generations_count'],
                            generations_max=camera_data['generations_max'])
            session.add(camera)
            session.flush()

            for keypoint_data in camera_data['keypoints']:
                keypoint = Keypoint(camera_name=camera_data['name'],
                                    x=keypoint_data['x'],
                                    y=keypoint_data['y'],
                                    size=keypoint_data['size'],
                                    angle=keypoint_data['angle'],
                                    response=keypoint_data['response'],
                                    octave=keypoint_data['octave'],
                                    fitness=keypoint_data['fitness'],
                                    number_of_generations=keypoint_data['number_of_generations'],
                                    distance=keypoint_data['distance'],
                                    avg_distance=keypoint_data['avg_distance'],
                                    step=keypoint_data['step'],
                                    descriptor=keypoint_data['descriptor'])
                session.add(keypoint)

        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Ошибка при записи в базу данных: {e}")
    finally:
        session.close()