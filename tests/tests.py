import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from database import insert_pets, get_pets, Base, Pet
from API import get_all_pets, remove_pet_by_id


class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Создаем временную базу данных в памяти для тестов
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        # Начинаем новую сессию базы данных перед каждым тестом
        self.session = self.Session()

    def tearDown(self):
        # Откатываем изменения и закрываем сессию после каждого теста
        self.session.rollback()
        self.session.close()

    @patch('API.get_all_pets')
    def test_insert_pets(self, mock_get_all_pets):
        # Задаем что функция get_all_pets вернет эти данные
        mock_get_all_pets.return_value = [
            {"name": "Dog", "status": "available"},
            {"name": "Cat", "status": "available"}
        ]

        # Создаем фейковую сессию базы данных
        mock_session = MagicMock(spec=Session)
        insert_pets(mock_session)
        # Проверяем что данные были сохранены в базу данных
        mock_session.commit.assert_called_once()

    @patch('builtins.print')
    def test_get_pets(self, mock_print):
        # Создаем двух питомцев и добавляем их в базу данных
        pet1 = Pet(name='Buddy', status='available')
        pet2 = Pet(name='Max', status='sold')
        self.session.add(pet1)
        self.session.add(pet2)
        self.session.commit()

        # Получаем питомцев из базы данных и проверяем что они правильно выводятся
        get_pets(self.session)
        mock_print.assert_any_call("ID: 1, Name: Buddy, Status: available")
        mock_print.assert_any_call("ID: 2, Name: Max, Status: sold")

class TestAPI(unittest.TestCase):
    @patch('requests.get')
    def test_get_all_pets(self, mock_get):
        # Создаем фейковый ответ от API
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": 1, "name": "Dog"}, {"id": 2, "name": "Cat"}]
        mock_get.return_value = mock_response

        # Проверяем что функция get_all_pets возвращает правильные данные
        result = get_all_pets()
        self.assertEqual(result, [{"id": 1, "name": "Dog"}, {"id": 2, "name": "Cat"}])

    @patch('builtins.input', side_effect=[1])
    @patch('requests.delete')
    def test_remove_pet_by_id(self, mock_delete, mock_input):
        # Создаем фейковый ответ от API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_delete.return_value = mock_response

        # Проверяем что функция remove_pet_by_id правильно удаляет питомца
        with patch('builtins.print') as mock_print:
            remove_pet_by_id()
            mock_delete.assert_called_once_with('https://petstore.swagger.io/v2/pet/1')
            mock_print.assert_called_with("Питомец успешно удален!")
