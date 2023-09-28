from datetime import datetime
import time
import concurrent.futures
from Private_setting import bd_name

DB_FILE = bd_name

import random
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import update
from sqlalchemy.orm import sessionmaker
import asyncio
from debug.bd_function import ORM_Statys, database_entry, ORM_Event
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
def all_camera(session, cameras):

    from debug.rotate.main import one_step
    time_d = datetime.now()
    # Разбиваем камеры на группы по 10
    camera_groups = [cameras[i:i + 10] for i in range(0, len(cameras), 10)]

    # Определяем оставшиеся камеры
    remaining_cameras = cameras[len(camera_groups) * 10:]
    def update_camera_data(time_d,cameras):
        results, ewent  = [], []
        for i in range(len(cameras)):
            t = one_step(cameras[i])
            if not t.turn:
                new_event = ORM_Event(
                    name="Поворот" + cameras[i].name,
                    datetime=datetime.now(),  # .strftime('%Y-%m-%d %H:%M:%S'),
                    enabled=1  # Здесь 1 означает, что событие включено
                )

                # Добавьте объект события в сессию и сделайте commit
                ewent.append(new_event)

            # time_difference = datetime.now() - time_d
            # # Извлекаем количество часов, минут и секунд из разницы во времени
            # hours, remainder = divmod(time_difference.total_seconds(), 3600)  # 3600 секунд в часе
            # minutes, seconds = divmod(remainder, 60)
            # print(t.name, f"Количество minut: {int(minutes)} seconds: {int(seconds)}")
            results.append(t)
        return (results, ewent)

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        all_results = []
        time_d = datetime.now()
        # Запускаем потоки для каждой группы камер
        for camera_group in camera_groups:
            future = executor.submit(update_camera_data,time_d, camera_group)
            all_results.append(future)

        # Запускаем потоки для оставшихся камер
        if remaining_cameras:
            future = executor.submit(update_camera_data,time_d, remaining_cameras)
            all_results.append(future)

        # Ждем завершения всех потоков и получаем результаты
        combined_results = []
        for future in concurrent.futures.as_completed(all_results):
            # print("future.result()", future.result())
            combined_results.extend(future.result())



    # for status_name, update_function in status_functions.items():
    #     update_function(session,random.randint(0, 1))
    # print(combined_results)
    results  = combined_results[0]
    ewent = combined_results[1]
    cameras = results
    for e in ewent:
        session.add(e)
    session.commit()
    database_entry(cameras)
    time_difference = datetime.now() - time_d
    # Извлекаем количество часов, минут и секунд из разницы во времени
    hours, remainder = divmod(time_difference.total_seconds(), 3600)  # 3600 секунд в часе
    minutes, seconds = divmod(remainder, 60)
    print("Статусы обновлены", f"Количество minut: {int(minutes)} seconds: {int(seconds)}")
    time.sleep(random.uniform(1.01, 0.01))

def tuning_statuses_async(session):
    # Функция 2: асинхронное обновление флагов в соответствии с логикой
    rows = session.query(ORM_Statys).all()
    for row in rows:
        # Проверяем флаг и вызываем соответствующую функцию
        if row.flag == 0:
            func = status_functions.get(row.name)
            print(row.name,status_functions.get(row.name))
            func(session, 1)
    print("Починили статусы")
    time.sleep(5)  # Подождать 60 секунд перед следующей проверкой

    # Основной асинхронный цикл
def main_async(session):
    cameras = read_from_database()
    #print("cameras",cameras)
    while True:
        all_camera(session, cameras)
        #print("cameras",cameras)
        # tuning_statuses_async(session)
        # Вызываем функции для обновления статусов


if __name__ == "__main__":
    main_async(session)
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main_async(session))