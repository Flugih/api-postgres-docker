# Используем официальный образ Python из Docker Hub
FROM python:3.9-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Обновляем pip
RUN pip install --upgrade pip

# Копируем файл requirements.txt в рабочую директорию
COPY requirements.txt .

# Устанавливаем зависимости для сборки psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта в рабочую директорию
COPY . .

# Копируем файл .env в рабочую директорию
COPY .env .env

# Указываем команду, которая будет выполнена при запуске контейнера
ENTRYPOINT ["python", "main.py"]