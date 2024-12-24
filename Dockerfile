# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем необходимые Python-пакеты
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем исходный код в контейнер
COPY . /app

# Устанавливаем рабочую директорию
WORKDIR /app

# Указываем команду для запуска бота
CMD ["python", "bot.py"]
