import os
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from API import API

Base = declarative_base()

# Определяем модель Pet для таблицы pets
class Pet(Base):
    __tablename__ = 'pets'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    status = Column(String, nullable=True)


class Database:
    def __init__(self):
        self.api = API()
        load_dotenv()

        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("Переменная окружения DATABASE_URL не установлена или пустая")

        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)  # Создание таблиц с использованием этого Base

    # Создание сессии
    def create_session(self):
        self.Session = sessionmaker(bind=self.engine)
        return self.Session()

    # Вставка питомцев в базу данных
    def insert_pets(self, session):
        try:
            # Получение данных от API
            data = self.api.get_all_pets()
            # Начало транзакции
            for pet in data:
                new_pet = Pet(name=pet.get('name'), status=pet.get('status'))
                session.add(new_pet)
            # Подтверждение транзакции
            session.commit()
        except Exception as ex:
            # Обработка ошибки и откат транзакции
            session.rollback()
            print(f"Ошибка при внесении данных в базу данных: {ex}")
        finally:
            # Закрытие сессии
            session.close()

    # Получение всех питомцев
    def display_pets(self, session):
        try:
            # Выполнение запроса к базе данных
            pets = session.query(Pet).all()
            # Итерация по результатам и вывод информации
            for pet in pets:
                print(f"ID: {pet.id}, Name: {pet.name}, Status: {pet.status}")
        except Exception as ex:
            # Обработка ошибки
            print(f"Ошибка при выполнении запроса к базе данных: {ex}")
        finally:
            # Закрытие сессии
            session.close()

    # Удаление питомца по его ID
    def delete_pet_by_id(self, session, pet_id):
        try:
            # Получение питомца по ID
            pet = session.query(Pet).filter_by(id=pet_id).first()
            if pet:
                # Удаление питомца
                session.delete(pet)
                session.commit()
                print(f"Питомец с ID: {pet_id} был удален.")
            else:
                print(f"Питомец с ID: {pet_id} не найден.")
        except Exception as ex:
            # Обработка ошибки и откат транзакции
            session.rollback()
            print(f"Ошибка при удалении питомца: {ex}")
        finally:
            # Закрытие сессии
            session.close()