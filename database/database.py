import os
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker
from API import get_all_pets

# Создаем базовый класс для декларативного определения таблиц
Base = declarative_base()

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем URL базы данных из переменных окружения
database_url = os.getenv("DATABASE_URL")

# Проверяем что переменная окружения DATABASE_URL установлена и не пустая
if not database_url:
    raise ValueError("Переменная окружения DATABASE_URL не установлена или пустая")

try:
    # Создаем движок для подключения к базе данных
    engine = create_engine(database_url)
    print("Подключение к базе данных успешно установлено")
except SQLAlchemyError as e:
    # Обрабатываем ошибки подключения к базе данных
    print(f"Ошибка при подключении к базе данных: {e}")

# Определяем модель Pet для таблицы pets
class Pet(Base):
    __tablename__ = 'pets'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    status = Column(String, nullable=True)

# Функция для создания новой сессии базы данных
def create_session():
    session = sessionmaker(bind=engine)
    return session()

# Функция для вставки питомцев в базу данных
def insert_pets(session):
    # Получаем данные о питомцах из API
    data = get_all_pets()
    if isinstance(data, list):
        for pet in data:
            # Создаем новый объект Pet и добавляем его в сессию
            new_pet = Pet(name=pet.get('name'), status=pet.get('status'))
            session.add(new_pet)
        # Сохраняем изменения в базе данных
        session.commit()

# Функция для получения всех питомцев из базы данных
def get_pets(session):
    # Получаем всех питомцев из базы данных
    pets = session.query(Pet).all()
    for pet in pets:
        # Выводим информацию о каждом питомце
        print(f"ID: {pet.id}, Name: {pet.name}, Status: {pet.status}")

# Функция для удаления питомца по его идентификатору
def delete_pet_by_id(session):
    pet_id = None

    try:
        # Получаем идентификатор питомца от пользователя
        pet_id = int(input("Введите айди питомца, которого хотите удалить: "))
    except ValueError:
        # Обрабатываем ошибку, если пользователь ввел не число
        print("Вы должны ввести число")
        return

    # Находим питомца по идентификатору
    pet = session.query(Pet).filter_by(id=pet_id).first()
    if pet:
        # Удаляем питомца из базы данных
        session.delete(pet)
        session.commit()
        print(f"Питомец с айди: {pet_id} был удален.")
    else:
        # Выводим сообщение, если питомец не найден
        print(f"Питомец с айди: {pet_id} не был найден")

# Создаем все таблицы в базе данных
Base.metadata.create_all(engine)
