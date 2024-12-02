import requests
import random

# Функция для получения всех доступных питомцев
def get_all_pets():
    # Отправляем GET-запрос к API для получения питомцев со статусом "available"
    response = requests.get("https://petstore.swagger.io/v2/pet/findByStatus?status=available")

    # Проверяем что запрос выполнен успешно
    if response.status_code == 200:
        data = response.json()

        # Проверяем что полученные данные являются списком
        if isinstance(data, list):
            return data
        else:
            print("Ошибка: данные не являются списком")
    else:
        # Выводим сообщение об ошибке если запрос не удался
        print(f"Ошибка при выполнении запроса: {response.status_code}")

# Функция для отображения всех доступных питомцев
def display_all_pets():
    # Получаем данные о питомцах
    data = get_all_pets()
    if isinstance(data, list):
        # Выводим информацию о каждом питомце
        for pet in data:
            print(f"Name: {pet.get('name')}")
            print(f"ID: {pet.get('id')}")
            print(f"Status: {pet.get('status')}")
            print("-" * 20)
    else:
        # Выводим сообщение об ошибке если данные не являются списком
        print("Ошибка: данные не являются списком")

# Функция для добавления нового питомца
def add_new_pet():
    while True:
        try:
            # Получаем имя питомца от пользователя
            name = input("Введите имя питомца: ")
            if name:
                # Формируем данные для запроса
                data_request = {
                    "id": 0,
                    "category": {
                        "id": 0,
                        "name": "string"
                    },
                    "name": name,
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
                response = requests.post("https://petstore.swagger.io/v2/pet", json=data_request)

                # Проверяем что запрос выполнен успешно
                if response.status_code == 200:
                    print("Питомец успешно добавлен!")
                else:
                    # Выводим сообщение об ошибке, если запрос не удался
                    print(f"Ошибка при добавлении питомца. Status code: {response.status_code}, Response: {response.text}")
                break

        except Exception as ex:
            # Обрабатываем любые исключения и выводим сообщение об ошибке
            print(f"Ошибка! {ex}")

# Функция для удаления питомца по его идентификатору
def remove_pet_by_id():
    while True:
        pet_id = 0
        try:
            # Получаем идентификатор питомца от пользователя
            while True:
                try:
                    pet_id = int(input("Введите айди питомца: "))
                    break
                except ValueError:
                    # Обрабатываем ошибку, если пользователь ввел не число
                    print("Вы должны ввести число!")

            if pet_id:
                # Отправляем DELETE-запрос к API для удаления питомца
                response = requests.delete(f"https://petstore.swagger.io/v2/pet/{pet_id}")

                # Проверяем что запрос выполнен успешно
                if response.status_code == 200:
                    print("Питомец успешно удален!")
                elif response.status_code == 400:
                    # Выводим сообщение об ошибке, если указан неверный идентификатор
                    print("Указан неверный идентификатор")
                elif response.status_code == 404:
                    # Выводим сообщение об ошибке если питомец не найден
                    print("Питомец не найден")
                break

        except Exception as ex:
            # Обрабатываем любые исключения и выводим сообщение об ошибке
            print(f"Ошибка! {ex}")
