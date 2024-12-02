import unittest
from API import display_all_pets, add_new_pet, remove_pet_by_id
from database import insert_pets, get_pets, delete_pet_by_id, create_session
from tests import TestDatabase, TestAPI

class TextUserInterface:
    def __init__(self):
        # Инициализация сессии базы данных
        self.session = create_session()

    def start_tui(self):
        # Основной цикл текстового интерфейса пользователя
        while True:
            # Отображение главного меню
            self.__show_menu("Главное меню", ["API", "DataBase", "Tests"])
            # Получение ввода пользователя и выполнение соответствующего действия
            match self.__get_input(3):
                case 1:
                    # Переход в меню с запросами
                    self.__tui_api()
                case 2:
                    # Переход в меню с взаимодействием с базой данных
                    self.__tui_database()
                case 3:
                    # Переход в меню с тестами базы данных и запросов
                    self.__tui_tests()

    def __tui_api(self):
        # Меню для работы с API
        while True:
            self.__show_menu("Меню с API", ["Получить список питомцев", "Добавить нового питомца", "Удалить питомца", "Назад"])
            match self.__get_input(4):
                case 1:
                    print("Получить список питомцев")
                    # Получние и вывод всех питомцев
                    display_all_pets()
                case 2:
                    print("Добавить нового питомца")
                    # Добавление нового питомца
                    add_new_pet()
                case 3:
                    print("Удалить питомца")
                    # Удаление питомца по его идентификатору
                    remove_pet_by_id()
                case 4:
                    # Вернуться в главное меню
                    print("Назад")
                    break

    def __tui_database(self):
        # Меню для работы с базой данных
        while True:
            self.__show_menu("Меню database", ["Сохранить список питомцев в базе данных", "Получить список питомцев из базы данных", "Удалить питомца из базы данных(по айди)", "Назад"])
            match self.__get_input(4):
                case 1:
                    print("Сохранить список питомцев в базе данных")
                    # Сохранение всех полученных питомцев в базе данных
                    insert_pets(self.session)
                case 2:
                    print("Получить список питомцев из базы данных")
                    # Получение и вывод всех питомцев
                    get_pets(self.session)
                case 3:
                    print("Удалить питомца из базы данных(по айди)")
                    # Удаление питомца из базы данных по его идентификатору
                    delete_pet_by_id(self.session)
                case 4:
                    # Вернуться в главное меню
                    print("Назад")
                    break

    def __tui_tests(self):
        # Меню для запуска тестов
        while True:
            self.__show_menu("Меню с тестами", ["test API", "test Database", "Назад"])
            match self.__get_input(3):
                case 1:
                    print("API")
                    # Запуск тестов API
                    self.run_test(TestAPI)
                case 2:
                    # Запуск тестов Database
                    print("DataBase")
                    self.run_test(TestDatabase)
                case 3:
                    # Вернуться в главное меню
                    print("Назад")
                    break

    def run_test(self, TestClass):
        # Запуск тестов с использованием unittest
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(TestClass)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)

    def __show_menu(self, title, options):
        # Отображение меню с заданным заголовком и опциями
        print()
        if title != "Главное меню":
            title = "Главное меню -> " + title
        print(title)
        # Перебор пунктов и их вывод
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")

    def __get_input(self, max_value):
        # Получение ввода пользователя с проверкой на корректность
        while True:
            try:
                move = int(input())
                # Проверка на ОДЗ
                if 1 <= move <= max_value:
                    return move
                else:
                    # Выво ошибки если введенное число было вне дипозона выбора
                    print(f"Число должно быть в диапозоне 1 - {max_value}")
            except Exception:
                # Вывод ошибки если было введено не число
                print(f"Вы должны ввести число! (1 - {max_value})")