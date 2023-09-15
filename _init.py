from sqlalchemy import create_engine, Column, Integer, Float, String, UniqueConstraint, Index, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# guid_url = f"http://{Private_setting.ip}/objects/?password={Private_setting.password}"
# response = requests.get(guid_url, verify=False)
#
# for i in json.loads(response.content):
#     name, guid = next(iter(i.items()))
#     t = Private_setting.Camera(name,guid,datetime.now().strftime("%Y-%m-%d %H:%M:%S") )
#     Private_setting.cameras.append(t)


# Создайте движок для подключения к базе данных SQLite
engine = create_engine('sqlite:///my_database.db')
# Создайте базовый класс для описания модели
Base = declarative_base()

# Определите модель для таблицы keypoints
class Keypoint(Base):
    __tablename__ = 'keypoints'
    id_u = Column(Integer, primary_key=True)
    id = Column(Integer)
    camera_id = Column(String)
    x = Column(Float)
    y = Column(Float)
    size = Column(Float)
    angle = Column(Float)
    response = Column(Float)
    octave = Column(Integer)
    fitness = Column(Float)
    number_of_generations = Column(Integer)
    distance = Column(Float)
    step = Column(Integer)
    descriptor = Column(String)
    avg_distance = Column(Float)

# Определите модель для таблицы cameras
class Camera(Base):
    __tablename__ = 'cameras'

    id = Column(Integer, primary_key=True)
    guids = Column(String, unique=True)
    name = Column(String)
    max_point = Column(Integer)

    # Определите уникальные ограничения и индексы
    __table_args__ = (
        UniqueConstraint('name', name='unique_camera_name'),
        Index('unique_name', 'name', unique=True),
    )

# Создайте таблицы в базе данных
Base.metadata.create_all(engine)

# Создайте сессию для взаимодействия с базой данных
Session = sessionmaker(bind=engine)
session = Session()

# Пример добавления данных в таблицу
new_camera = Camera(guids='guid123', name='Camera 1', max_point=100)
session.add(new_camera)
session.commit()

# Закройте сессию
session.close()
