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
    id = Column(Integer, primary_key=True)
    name = Column(String)
    guid = Column(String)
    angle = Column(Float)
    datetime = Column(String)  # Подставьте нужный тип данных
    keypoint_count = Column(Integer)
    generations_count = Column(Integer)
    generations_max = Column(Integer)
    old = Column(String)  # Подставьте нужный тип данных
    status_code = Column(Integer)
    content_type = Column(String)  # Подставьте нужный тип данных
    turn = Column(Integer)

    # Связь с ключевыми точками
    keypoints = relationship('Keypoint', back_populates='camera')

# Определяем модель данных (таблицу) Keypoint
class Keypoint(Base):
    __tablename__ = 'keypoints'
    id = Column(Integer, primary_key=True)
    camera_id = Column(Integer, ForeignKey('cameras.id'))
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

def database_entry(cameras): pass


# Функция для считывания всех камер и их ключевых точек
def read_from_database():

    Session = sessionmaker(bind=engine)
    session = Session()

    # Считываем все камеры в базе данных
    cameras = session.query(Camera).all()

    # Для каждой камеры считываем соответствующие ключевые точки
    for camera in cameras:
        keypoints = session.query(Keypoint).filter_by(camera_id=camera.id).all()
        camera.old = keypoints

    session.close()

    return cameras

def update_guides_in_bd(): pass
