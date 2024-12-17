import argparse
import unittest
from API import API
from database import Database
from tests import TestDatabase, TestAPI


class CommandLineInterface:
    def __init__(self):
        # Инициализация объектов API и Database
        self.api = API()
        self.db = Database()

        # Создание сессии для работы с базой данных
        self.session = self.db.create_session()

        # Создание парсера аргументов командной строки
        self.parser = argparse.ArgumentParser(description="Pet Manager")

        # Добавление подкоманд для парсера
        self.subparsers = self.parser.add_subparsers(dest="command", required=True)

    def run_test(self, test_name):
        # Запуск тестов в зависимости от имени теста
        if test_name.lower() == "api":
            self._run_test(TestAPI)
        elif test_name.lower() == "database":
            self._run_test(TestDatabase)

    def _run_test(self, TestClass):
        # Загрузка и запуск тестов из указанного класса тестов
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(TestClass)
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)

    def parse_args(self):
        # Добавление подкоманд и их аргументов
        self.subparsers.add_parser("display_pets_api", help="Display all pets")

        add_parser = self.subparsers.add_parser("add_api", help="Add a new pet")
        add_parser.add_argument("name", type=str, help="Name of the pet")

        delete_api_parser = self.subparsers.add_parser("delete_pet_api", help="Delete a pet by ID via API")
        delete_api_parser.add_argument("pet_id_api", type=int, help="ID of the pet to delete")

        test_parser = self.subparsers.add_parser("test", help="Run tests")
        test_parser.add_argument("test_name", choices=["api", "database"], help="Run API or Database tests")

        self.subparsers.add_parser("insert_database", help="Insert pets into the database")

        self.subparsers.add_parser("display_pets_database", help="Retrieve all pets from the database")

        delete_db_parser = self.subparsers.add_parser("delete_pet_database", help="Delete a pet by ID in the database")
        delete_db_parser.add_argument("pet_id_db", type=int, help="ID of the pet to delete")

        # Парсинг аргументов командной строки
        return self.parser.parse_args()

    def execute_command(self, args):
        # Выполнение команды в зависимости от аргументов
        if args.command == "display_pets_api":
            self.api.display_all_pets()
        elif args.command == "add_api":
            self.api.add_new_pet(args.name)
        elif args.command == "delete_pet_api":
            self.api.remove_pet_by_id(args.pet_id_api)
        elif args.command == "test":
            self.run_test(args.test_name)
        elif args.command == "insert_database":
            self.db.insert_pets(self.session)
        elif args.command == "display_pets_database":
            self.db.display_pets(self.session)
        elif args.command == "delete_pet_database":
            self.db.delete_pet_by_id(self.session, args.pet_id_db)
        else:
            # Вывод справки, если команда не распознана
            self.parser.print_help()
