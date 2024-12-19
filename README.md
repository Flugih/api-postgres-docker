Pet Management System:

Pet Management System — это проект, который позволяет взаимодействовать с API сайта для управления списком питомцев. Проект использует `requests` для отправки API запросов, `Docker` для контейнеризации базы данных и `SQLAlchemy` для взаимодействия с базой данных.

Требования:

- Docker
- Python 3.x
- pip

Шаги установки:

1. Создать виртуальную среду(venv) в папке с проектом:
cd "project_path"
python -m venv venv

2. Установка зависимостей
pip install -r requirements.txt

3. Запустить Docker контейнеры:
docker-compose up -d

4. Настройка переменные окружения и docker-compose.yml:
Обновить данные в .env файле исходя из внесенных изменений в docker_compose.yml

5. Запуск проекта:
Запустить start.bat для начала пользования сервисом
		