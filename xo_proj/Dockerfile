# 1. Используем официальный образ Python как базовый
FROM python:3.12-slim

# 2. Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# 2.1 Устанавливаем зависимости системы, включая curl
RUN apt-get update && apt-get install -y curl && apt-get clean && rm -rf /var/lib/apt/lists/*

# 3. Копируем файл зависимостей в контейнер
COPY requirements.txt .

# 4. Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копируем весь проект в контейнер
COPY src/ .

# 6. Указываем команду для запуска приложения
CMD ["python3", "app.py"]

# 7. (Опционально) Если приложение использует конкретный порт, указываем его
EXPOSE 5000
