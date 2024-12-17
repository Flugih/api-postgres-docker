from os import getenv
import requests
from dotenv import load_dotenv

# Функция для получения всех доступных питомцев
class API:
    def __init__(self):
        load_dotenv()
        self.api_base_url = getenv("API_BASE_URL")
        self.api_get_endpoint_url = getenv("API_GET_ENDPOINT_URL")
        self.api_remove_endpoint_url = getenv("API_REMOVE_ENDPOINT_URL")
        self.api_add_endpoint_url = getenv("API_ADD_ENDPOINT_URL")

        if not self.api_base_url:
            raise ValueError("Переменная API_BASE_URL не установлена")
        if not self.api_get_endpoint_url:
            raise ValueError("Переменная API_GET_ENDPOINT_URL не установлена")
        if not self.api_remove_endpoint_url:
            raise ValueError("Переменная API_REMOVE_ENDPOINT_URL не установлена")
        if not self.api_add_endpoint_url:
            raise ValueError("Переменная API_ADD_ENDPOINT_URL не установлена")

    def get_full_url(self, endpoint):
        # Определение полной ссылки
        return f"{self.api_base_url}/{endpoint}"

    def get_all_pets(self):
        data = None
        # Отправляем GET-запрос к API для получения питомцев со статусом "available"
        response = requests.get(self.get_full_url(self.api_get_endpoint_url))

        # Проверяем что запрос выполнен успешно
        if response.status_code == 200:
            data = response.json()
        else:
            # Выводим сообщение об ошибке если запрос не удался
            print(f"Ошибка при выполнении запроса: {response.status_code}")

        # Проверяем что полученные данные являются списком
        if isinstance(data, list):
            return data
        else:
            print("Ошибка: данные не являются списком")

    # Функция для отображения всех доступных питомцев
    def display_all_pets(self):
        # Получаем данные о питомцах
        data = self.get_all_pets()
        # Выводим информацию о каждом питомце
        for pet in data:
            print(f"Name: {pet.get('name')}")
            print(f"ID: {pet.get('id')}")
            print(f"Status: {pet.get('status')}")
            print("-" * 20)

    # Функция для добавления нового питомца
    def add_new_pet(self, pet_name):
        # Формируем данные для запроса
        data_request = {
            "id": 0,
            "category": {
                "id": 0,
                "name": "string"
            },
            "name": pet_name,
            "photoUrls": [
                "string"
            ],
            "tags": [
                {
                    "id": 0,
                    "name": "string"
                }
            ],
            "status": "available"
        }

        # Отправляем POST-запрос к API для добавления нового питомца
        response = requests.post(self.get_full_url(self.api_add_endpoint_url), json=data_request)

        # Проверяем что запрос выполнен успешно
        if response.status_code == 200:
            print("Питомец успешно добавлен!")
        else:
            # Выводим сообщение об ошибке, если запрос не удался
            print(f"Ошибка при добавлении питомца. Status code: {response.status_code}, Response: {response.text}")

    # Функция для удаления питомца по его идентификатору
    def remove_pet_by_id(self, pet_id):
        # Отправляем DELETE-запрос к API для удаления питомца
        response = requests.delete(self.get_full_url(self.api_remove_endpoint_url) + str(pet_id))

        # Проверяем что запрос выполнен успешно
        if response.status_code == 200:
            print("Питомец успешно удален!")
        elif response.status_code == 400:
            # Выводим сообщение об ошибке, если указан неверный идентификатор
            print("Указан неверный идентификатор")
        elif response.status_code == 404:
            # Выводим сообщение об ошибке если питомец не найден
            print("Питомец не найден")

