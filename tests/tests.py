import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Database, Pet, Base
from API import API


class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        db = Database()  # Создание экземпляра базы данных

        cls.engine = create_engine('sqlite:///:memory:')  # В памяти
        Base.metadata.create_all(cls.engine)  # Создание всех таблиц в базе данных в памяти

        # Создаем сессию
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()

    def setUp(self):
        # Начинаем новую сессию перед каждым тестом
        self.session = self.Session()

        # Очищаем базу данных перед каждым тестом
        self.session.query(Pet).delete()
        self.session.commit()

    def tearDown(self):
        # Откатываем изменения и закрываем сессию после каждого теста
        self.session.rollback()
        self.session.close()

    @patch('API.API')
    def test_insert_pets(self, mock_get_all_pets):
        db = Database()

        # Мокаем API для получения питомцев
        db.api.get_all_pets = MagicMock(return_value=[
            {"name": "Dog", "status": "available"},
            {"name": "Cat", "status": "available"}
        ])

        # Вставляем питомцев в базу данных
        db.insert_pets(self.session)

        # Проверяем, что питомцы были вставлены
        pets = self.session.query(Pet).all()
        self.assertEqual(len(pets), 2)
        self.assertEqual(pets[0].name, 'Dog')
        self.assertEqual(pets[0].status, 'available')
        self.assertEqual(pets[1].name, 'Cat')
        self.assertEqual(pets[1].status, 'available')

    def test_display_pets(self):
        db = Database()
        # Создаем двух питомцев
        pet1 = Pet(name='Buddy', status='available')
        pet2 = Pet(name='Max', status='sold')
        self.session.add(pet1)
        self.session.add(pet2)
        self.session.commit()

        # Получаем питомцев из базы данных
        pets = self.session.query(Pet).all()

        # Проверяем, что питомцы правильно сохранены
        self.assertEqual(len(pets), 2)
        self.assertEqual(pets[0].name, 'Buddy')
        self.assertEqual(pets[0].status, 'available')
        self.assertEqual(pets[1].name, 'Max')
        self.assertEqual(pets[1].status, 'sold')


class TestAPI(unittest.TestCase):
    @patch('requests.post')
    def test_add_new_pet(self, mock_post):
        api = API()
        # Создаем фейковый ответ от API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Проверяем что функция add_new_pet правильно добавляет питомца
        with patch('builtins.print') as mock_print:
            api.add_new_pet("Buddy")
            mock_post.assert_called_once()
            mock_print.assert_called_with("Питомец успешно добавлен!")

    @patch('requests.delete')
    def test_remove_pet_by_id(self, mock_delete):
        api = API()
        # Создаем фейковый ответ от API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_delete.return_value = mock_response

        # ID питомца, который будет передан в метод
        pet_id = 1

        # Проверяем что функция remove_pet_by_id правильно удаляет питомца
        with patch('builtins.print') as mock_print:
            api.remove_pet_by_id(pet_id)
            mock_delete.assert_called_once_with(f'{api.get_full_url(api.api_remove_endpoint_url)}{pet_id}')
            mock_print.assert_called_with("Питомец успешно удален!")
