# Используем официальный Python образ
FROM python:3.11-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --upgrade pip && \
    grep -v '^#' requirements.txt | grep -v '^$' > /tmp/requirements_clean.txt && \
    pip install --no-cache-dir -r /tmp/requirements_clean.txt

# Копируем исходный код и данные
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY knowledge_base/ ./knowledge_base/
COPY data/vector_db/ ./data/vector_db/

# Создаём необходимые директории
RUN mkdir -p logs data/new_docs

# Переменные окружения
ENV PYTHONUNBUFFERED=1
ENV TRANSFORMERS_CACHE=/app/.cache/huggingface

# Команда запуска Telegram бота
CMD ["python", "src/telegram_bot_local.py"]
