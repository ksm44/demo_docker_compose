# Домашнее задание к лекции «Docker Compose»

Cделать конфигурацию docker-compose любого Вашего проекта из части по Django, который использует БД

Результатом является docker-compose.yml файл с описанием конфигурации для развертывания приложения (и не забудьте про Dockerfile).

P.S. для создания конфигурации необходим образ своего проекта, а значит предварительно необходимо описать Dockerfile, сделать образ и потом уже писать docker-compose.yml (это типичный сценарий при работе с Docker и Docker Compose).

Подсказка:
Конфигурация должна состоять из 3-х контейнеров: backend, postgres, nginx.

Контейнеры объединяются в сеть, которые работают в связке:

Nginx работает в качестве proxy-http для пересылки динамических запросов к Django или возвращая статические html файлы.
PostgreSQL запускается до Django.
Django запускается через Gunicorn.

# Что пришлось сделать на сервере чтобы всё заработало
1. Клонировать репозиторий
```bash
cd /opt
git clone https://github.com/ksm44/demo_docker_compose.git
cd demo_docker_compose/demo_docker_compose
```

2. Починить docker compose (v2 не подхватился):

```bash
sudo ln -sf /usr/libexec/docker/cli-plugins/docker-compose /usr/local/bin/docker-compose
```
→ теперь работает docker-compose (через дефис).

3. Создать/поправить .env
```yaml
DB_HOST=postgres (не localhost)

DB_NAME = POSTGRES_DB (совпадение имён!)

SECRET_KEY без $ (иначе Compose портит подстановкой)

DEBUG=False

ALLOWED_HOSTS=194.58.102.17,localhost,127.0.0.1

CSRF_TRUSTED_ORIGINS=http://194.58.102.17
```
4. Поправить docker-compose.yml

Том postgres: pgdata:/var/lib/postgresql (в PG 18 новый путь — без /data)

command backend — одной строкой:

```yaml
sh -c "python manage.py migrate &&
       python manage.py collectstatic --noinput &&
       exec gunicorn demo_docker_compose.asgi:application --bind 0.0.0.0:8000"
(флаг --worker-class uvicorn... убрали, чтобы не ставить лишний пакет)
```
5. Поправить nginx.conf

```nginx
proxy_set_header Host $host;
```
(иначе Django ругался DisallowedHost: backend:8000)

6. Поправить settings.py
```yaml
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')

CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS').split(',')

STATIC_ROOT = BASE_DIR / 'static'
```
7. Сбросить старые тома (созданы с неправильной структурой)

```bash
docker-compose down -v
```
8. Запустить

```bash
docker-compose up --build -d
docker-compose ps        # всё Up
curl http://127.0.0.1/
```
Главные грабли:

PostgreSQL 18 → путь тома без /data

.env с $ в SECRET_KEY → Compose ломает значение

DB_HOST=localhost внутри контейнера ≠ хост-машина

DB_NAME ≠ POSTGRES_DB → БД «не существует»

command многострочный → sh ломает аргументы

nginx не передавал Host → DisallowedHost

CSRF-токен и CSRF_TRUSTED_ORIGINS для домена/IP