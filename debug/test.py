import sqlite3
from Private_setting import bd_name

DB_FILE = bd_name
# Подключение к базе данных SQLite (создаст файл базы данных, если его нет)
conn = sqlite3.connect(F'{DB_FILE}.db')

# Создание курсора для выполнения SQL-запросов
cursor = conn.cursor()
for i in range(6,221):
    # Данные, которые вы хотите вставить
    data = (f'Окно {i}', 'Axqo72v1', 45.0, '2023-09-15 12:00:00', 10, 5, 20)

    # SQL-запрос для вставки данных
    insert_query = """
    INSERT INTO cameras (name, guid, angle, datetime, keypoint_count, generations_count, generations_max)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    # Выполнение SQL-запроса с данными
    cursor.execute(insert_query, data)

    # Фиксация изменений в базе данных
    conn.commit()

# Закрытие курсора и соединения
cursor.close()
conn.close()