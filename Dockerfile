FROM python:3.11-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Устанавливаем зависимости напрямую, без requirements.txt
RUN pip install --no-cache-dir \
    aiogram==3.13.1 \
    openai>=1.35.0 \
    python-dotenv>=1.0.1

# Копируем весь проект
COPY . .

# Команда запуска бота
CMD ["python", "main.py"]
