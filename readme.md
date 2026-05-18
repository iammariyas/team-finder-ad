# TeamFinder
_**TeamFinder**_ - это место встречи разработчиков, дизайнеров и всех, кто хочет создавать pet-проекты в команде. 
Публикуйте идеи проектов, добавляйте в избранное понравившиеся, находите единомышленников и откликайтесь на предложения других специалистов.

## Требования

- Python 3.9+
- Docker и Docker Compose (для PostgreSQL)
- Файл `requirements.txt` в корне проекта

## Быстрый запуск

### 1. Клонирование и окружение

```bash
git clone https://github.com/iammariyas/team-finder-ad.git
```

```bash
cd team-finder-ad
python -m venv venv
```

Windows (PowerShell): `venv\Scripts\Activate.ps1`  
Linux/macOS: `source venv/bin/activate`

```bash
pip install -r requirements.txt
```

### 2. Переменные окружения

Скопируйте пример и при необходимости отредактируйте:

```bash
cp .env_example .env
```
После этого откройте .env и укажите свои значения.

| Переменная            | Назначение                                                                                                                                                 |
|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **DJANGO_SECRET_KEY** | Секретный ключ Django, используемый для подписи cookie и токенов. Можно сгенерировать при помощи `get_random_secret_key` из `django.core.management.utils` |
| **DJANGO_DEBUG**      | Режим отладки. Установите `True` во время разработки.                                                                                                      |
| **POSTGRES_DB**       | Имя базы данных PostgreSQL, которую будет использовать Django.                                                                                             |
| **POSTGRES_USER**     | Имя пользователя PostgreSQL.                                                                                                                               |
| **POSTGRES_PASSWORD** | Пароль пользователя PostgreSQL.                                                                                                                            |
| **POSTGRES_HOST**     | Адрес сервера БД. В случае локальной разработки localhost.                                                                                                 |
| **POSTGRES_PORT**     | Порт подключения к БД (по умолчанию `5432`).                                                                                                               |
| **TASK_VERSION**      | Номер варианта вашего задания. Используется для определения набора HTML-шаблонов.                                                                          |

### 3. База данных (Docker Compose)

Для работы приложения **TeamFinder** используется база данных **PostgreSQL**.
По условию задания база данных должна запускаться в контейнере Docker.

В проекте уже есть пример файла `docker-compose.yml`. 
```bash
docker compose up -d
```

Данные БД хранятся в именованном volume **`postgres_data`** и сохраняются при перезапуске контейнера.

Проверка готовности:

```bash
docker compose ps
docker compose logs db
```

### 4. Миграции и демо-данные

```bash
python manage.py migrate
python manage.py load_demo
```

Команда **`load_demo`** создаёт трёх пользователей с email `demo1@example.com`, `demo2@example.com`, `demo3@example.com` и по одному открытому проекту у каждого (повторный запуск безопасен: записи не дублируются). Пароль для всех демо-аккаунтов: **`demo12345`**.

Суперпользователь для админки (по желанию):

```bash
python manage.py createsuperuser
```

### 5. Запуск сервера

```bash
python manage.py runserver
```

Откройте в браузере: **http://127.0.0.1:8000/** (редирект на список проектов).

## Полезные URL

| Назначение | Путь |
|------------|------|
| Список проектов | `/projects/list/` |
| Вход | `/users/login/` |
| Регистрация | `/users/register/` |
| Список пользователей | `/users/list/` |
| Избранное (только для своего аккаунта) | `/projects/favorites/` |
| Админ-панель | `/admin/` |

## Стек

- Django, PostgreSQL, `python-decouple`, Pillow, `psycopg2-binary`.
___
Был реализован 1 вариант