from Private_setting import bd_name

DB_FILE = bd_name

import random
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import update
from sqlalchemy.orm import sessionmaker
import asyncio
from debug.bd_function import ORM_Statys, database_entry
from debug.bd_function import read_from_database
# # Создание базового класса моделей для SQLAlchemy
# Base = declarative_base()
#
# # Определение модели для таблицы statys
# class Statys(Base):
#     __tablename__ = 'statys'
#     name = Column(String, primary_key=True)
#     flag = Column(Integer)

# Создание подключения к базе данных
engine = create_engine(F'sqlite:///{DB_FILE}.db')
# Base.metadata.create_all(engine)

# Создание сессии SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()
# Функции для обновления статусов
# Функция для обновления статуса пароля
def update_password_status(session: Session, new_status: int):
    try:
        # Ищем запись с именем 'password' и обновляем флаг

        session.query(ORM_Statys).filter_by(name='password').update({'flag': new_status})
        session.commit()
        print("Статус пароля обновлен успешно.")
    except Exception as e:
        session.rollback()
        print(f"Ошибка при обновлении статуса пароля: {str(e)}")

# Функция для обновления статуса GUID
def update_guid_status(session: Session, new_status: int):

    try:
        # Ищем запись с именем 'guid' и обновляем флаг
        session.query(ORM_Statys).filter_by(name='guid').update({'flag': new_status})
        session.commit()
        print("Статус GUID обновлен успешно.")
    except Exception as e:
        session.rollback()
        print(f"Ошибка при обновлении статуса GUID: {str(e)}")

# Словарь статусов и соответствующих функций
status_functions = {
    'password': update_password_status,
    'guid': update_guid_status
}
async def all_camera(session, cameras):

    from debug.rotate.main import one_step
    for i in range(len(cameras)):
        cameras[i] = one_step(cameras[i])
        if not cameras[i].content_type:
            print("cameras[i].content_type")

        database_entry(cameras)
        print("все камеры")

    # for status_name, update_function in status_functions.items():
    #     update_function(session,random.randint(0, 1))
    print("Статусы обновлены.")
    await asyncio.sleep(random.uniform(0.5, 5.0))

async def tuning_statuses_async(session):
    # Функция 2: асинхронное обновление флагов в соответствии с логикой
    rows = session.query(ORM_Statys).all()
    for row in rows:
        # Проверяем флаг и вызываем соответствующую функцию
        if row.flag == 0:
            func = status_functions.get(row.name)
            print(row.name,status_functions.get(row.name))
            func(session, 1)
    print("Починили статусы")
    await asyncio.sleep(5)  # Подождать 60 секунд перед следующей проверкой

    # Основной асинхронный цикл
async def main_async(session):
    cameras = read_from_database()
    while True:
        await all_camera(session, cameras)
        await tuning_statuses_async(session)
        # Вызываем функции для обновления статусов


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_async(session))