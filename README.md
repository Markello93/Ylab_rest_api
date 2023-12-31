# REST API по работе с меню ресторана

## Краткое описание задачи


REST API по работе с меню ресторана со всеми CRUD операциями.
Зависимости:

●У меню есть подменю, которые к ней привязаны.

●У подменю есть блюда.

## Краткое описание структуры проекта

Сервис построен на трёхуровневой архитектуре и состоит из:
1. слой представления (директория `/api`): получение и валидация данных, формирование ответов.
2. слой бизнес-логики (директория `/service`). используется для работы с методами репозиториев
3. слой данных (директория `/repositories`): отвечает за операции с данными
   в БД.

Такая архитектура выбрана для упрощенного масштабирования проекта в будущем.
Все доступные CRUD операции прописаны в документации по пути /docs.

В проекте реализовано кэширование с помощью redis.

Создана задача в celery для синхронизации базы данных из excel файла Menu.xlsx (расположен в папке admin)

### Добавленный эндпоинт  в  ДЗ 4 для вывода всех объектов в базе:
* {{LOCAL_URL}}/api/v1/menus/menus_info/
## Инструкция по запуску проекта
```bash
git clone https://github.com/Markello93/Ylab_rest_api.git

#### Переменные окружения
Для работы приложения необходимы следующие переменные окружения
(необходимо создать файл `.env` в корневой директории проекта)
# Общие настройки
DB_HOST=postgres-rest  # имя хоста (контейнера) базы данных
DB_PORT=5432    # порт, на котором работает база данных
# Настройки контейнера базы данных
POSTGRES_USER=postgres      # имя суперпользователя postgres
POSTGRES_PASSWORD=postgres  # пароль суперпользователя
# Настройки приложения cargo
RESTO_APP_DB_NAME=postgres                     # название БД
RESTO_APP_DB_USER=postgres                     # имя пользователя БД сервиса
RESTO_APP_DB_PASSWORD='пароль от базы данных'  # Пароль пользователя БД
# Настройки тестового контейнера
DB_HOST_TEST=tests_db                   # имя хоста (контейнера) БД
DB_PORT_TEST=6000                       # порт для запуска тестовой БД
DB_NAME_TEST=postgres                   # название тестовой БД
DB_USER_TEST=postgres                   # имя пользователя тестовой БД
DB_PASS_TEST='пароль от базы данных'    # Пароль пользователя БД
# Настройки для подключения Redis для тестового контейнера и основного проекта
REDIS_HOST=redis                         # название тестовой БД redis
REDIS_PORT=6379                         # порт, на котором работает Бд
REDIS_CACHE_LIFETIME = 360              # время хранения кэша
REDIS_DB=0                              # номер БД Redis
# Настройки для подключения RabbitMQ как брокера Celery у основного проекта
RABBITMQ_DEFAULT_USER=guest              # пользователь RabbitMQ
RABBMQHOST=rabbitmq                      # хост RabbitMQ
RABBITMQ_DEFAULT_PASS=guest              # пароль пользователя RabbitMQ
```
#### Запуск сборку контейнеров для тестирования в postman:
Для тестирования функционала БД в postman необходимо сначала поднять приложение без включенных контейнеров celery и celery_beat.
Предлагается это делать командой:
```
docker-compose up -d resto_back postgres redis rabbitmq
```
Таким образом мы можем пройти тесты в postman без запуска фоновой задачи по обновлению БД
и затем подключить недостающие контейнеры для обновления:
```
docker-compose up -d --no-deps celery celery_beat
```
#### Запуск сборки контейнеров с подключенной фоновой задачей docker командой:
```
docker-compose up -d
```

В Dockerfile использован скрипт entrypoint.sh в котором запускается начальная миграция alembic с созданием таблиц в БД, после чего происходит запуск проекта.
Так же в Dockerfile прописана инструкция для автоматической установки зависимостей через менеджер poetry.

#### Для автоматического запуска тестов в отдельном контейнере используется команда:
```
docker-compose -f docker-compose_tests.yml up --abort-on-container-exit && docker-compose -f docker-compose_tests.yml  down -v
```
Команда поднимает контейнер, выполняет тесты, после чего удаляет контейнеры и тома.
## Стек технологий, использованных в проекте
* python 3.10
* fastapi
* pydantic
* alembic
* asyncpg
* uvicorn
* python-dotenv
* poetry
* PostgreSQL
* celery
* redis
