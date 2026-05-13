# Python 3.12, мінімальний образ
FROM python:3.12-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# в dockerignore ми заборонили ігнорувати файл 
COPY . . 

# Запуск пайплайну в ipynb автоматично, без відкриття вікна з ноутбуком в браузері
CMD ["jupyter", "nbconvert", "--to", "notebook", "--execute", "lesson_13_pipeline.ipynb"]

