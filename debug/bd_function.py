from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, relationship, DeclarativeBase

from Private_setting import bd_name



# Создаем подключение к базе данных SQLite
engine = create_engine(f'sqlite:///{bd_name}.db')
# Создаем базовый класс для описания моделей
# class Base(DeclarativeBase):pass
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class Statys(Base):
    __tablename__ = 'statys'
    name = Column(String, primary_key=True)
    flag = Column(Integer)
# Определяем модель данных (таблицу) Camera




