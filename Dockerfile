FROM python:3.11-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Сначала зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Потом весь остальной код
COPY . .

# Команда запуска бота
CMD ["python", "main.py"]
