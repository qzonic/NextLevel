# CI/CD
![Workflow](https://github.com/qzonic/NextLevel/actions/workflows/main.yml/badge.svg)

# Стек
<img src="https://img.shields.io/badge/Python-4169E1?style=for-the-badge"/> <img src="https://img.shields.io/badge/Django-008000?style=for-the-badge"/> <img src="https://img.shields.io/badge/DRF-800000?style=for-the-badge"/> <img src="https://img.shields.io/badge/Docker-00BFFF?style=for-the-badge"/> <img src="https://img.shields.io/badge/PostgreSQL-87CEEB?style=for-the-badge"/> <img src="https://img.shields.io/badge/Nginx-67c273?style=for-the-badge"/> <img src="https://img.shields.io/badge/Gunicorn-06bd1e?style=for-the-badge"/>

# Описание проекта:

**Проект Phonebook**

Проект представляет из себя простое API для работы с записной книгой, которое позволит:
* Добавлять новые контакты.
* Удалять контакты по идентификатору.
* Получать список всех контактов.
* Получать контакт по идентификатору.
* Обновлять контакт по идентификатору.

Дополнительно было реализоавнно:
* Возможность поиска контактов по имени или фамилии.
* Пагинацию для списка контактов.

Открыть проект в интернете [тык](http://188.225.33.53/api/v1/).


# Реализация

1. Фреймворки: проект основан на фреймворках Django и Django Rest.
2. Модели: реализована одна модель `Contact`, имеющая следующие поля:
   * id - уникальный идентификатор контакта;
   * owner - пользователь, добавящий контакт;
   * first_name - имя контакта;
   * last_name - фамилия контакта;
   * phone - телефон контакта;
   * email - почта контакта.
3. Работа с контактами: пользователь может взаимодействовать только с теми контактами, которые он добавил.
4. Тесты: в проекте написаны тесты, которые находятся в приложении `api`, для проверки реализованного функционала.
5. Инфраструктура: для упрощения работы с проектом были реализованы следующие пункты:
   * проект развернут в докере, используется `Dockerfile` и `docker-compose.yml`;
   * образ проекта хранится в `DockerHub`;
   * для упрощения деплоя настроена автоматизации в `CI/CD`.

# Как запустить проект:

*Клонировать репозиторий и перейти в него в командной строке:*
```
https://github.com/qzonic/NextLevel.git
```
```
cd NextLevel/
```

В директории NextLevel нужно создать .env файл, в котором указывается 
SECRET_KEY, HOST, DB_NAME, POSTGRES_USER, POSTGRES_PASSWORD, DB_HOST, DB_PORT.
Например:
```
SECRET_KEY='django-insecure-w2rvabrrx4_u=qfar0k*%zumx3l*d8@+v==%0o-i8k3(&9ut^='
DEBUG=False
HOST=188.225.33.53

DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=127.0.0.1
DB_PORT=5432
```

*Теперь необходимо собрать Docker-контейнеры:*
```
docker-compose up -d
```

*После сборки контейнеров, нужно прописать следующие команды по очереди:*
```
docker-compose exec web python3 manage.py migrate
```

```
docker-compose exec web python3 manage.py createsuperuser
```

```
docker-compose exec web python3 manage.py collectstatic --no-input
```

*Теперь проект доступен по адресу:*
```
http://127.0.0.1/
```

*Эндпоинты для взаимодействия с API можно посмотреть в документации по адресу:*
```
/api/v1/redoc/
```

### Автор
[![telegram](https://img.shields.io/badge/Telegram-Join-blue)](https://t.me/qzonic