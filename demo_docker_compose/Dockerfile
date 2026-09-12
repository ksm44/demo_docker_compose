#  Образы можно взять с hub.docker.com - это один из реестров (хранилищ) Docker-образов, причем официальный
FROM python:3.13.2-alpine3.21

# Откуда запускать приложение в контейнере
WORKDIR /app

# Копируем из локальной папки в контейнер
COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

# Просто указывем явно, что наше приложение использует порт 8000
EXPOSE 8000

CMD ["gunicorn", "demo_docker_compose.asgi:application", "--bind", "0.0.0.0:8000", "--worker-class", "uvicorn.workers.UvicornWorker"]