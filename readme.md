# TeamFinder
**TeamFinder** - это место встречи разработчиков, дизайнеров и всех, кто хочет создавать pet-проекты в команде. 
Публикуйте идеи проектов, добавляйте понравившиеся в избранное, находите единомышленников и 
откликайтесь на предложения других специалистов

___

# Первоначальная настройка проекта TeamFinder

## Требования
- Python 3.9+
- Docker и Docker Compose
- Git

## Установка
```bash
git clone https://github.com/iammariyas/team-finder-ad.git
cd team-finder-ad
```
## 1. Виртуальное окружение

Перед началом работы необходимо создать и активировать виртуальное окружение Python.  


1. **Создайте виртуальное окружение (в папке проекта):**
   ```bash
   python3 -m venv venv
   ```

2. **Активируйте окружение:**
    - **Windows (PowerShell):**
      ```bash
      venv\Scripts\Activate.ps1
      ```
    - **Windows (cmd):**
      ```bash
      venv\Scripts\activate
      ```
    - **Linux/Mac:**
      ```bash
      source venv/bin/activate
      ```

3. **Установите зависимости из `requirements.txt`:**
   ```bash
   pip install -r requirements.txt
   ```

## 2. Создание `.env`

В репозитории есть пример `.env_example`, который нужно скопировать и заполнить:

```bash
cp .env_example .env
```

После этого откройте `.env` и укажите свои значения.  

| Переменная            | Назначение                                                                                                                                                 |
|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **DJANGO_SECRET_KEY** | Секретный ключ Django, используемый для подписи cookie и токенов. Можно сгенерировать при помощи `get_random_secret_key` из `django.core.management.utils` |
| **DJANGO_DEBUG**      | Режим отладки. Установите `True` во время разработки.                                                                                                      |
| **POSTGRES_DB**       | Имя базы данных PostgreSQL, которую будет использовать Django.                                                                                             |
| **POSTGRES_USER**     | Имя пользователя PostgreSQL.                                                                                                                               |
| **POSTGRES_PASSWORD** | Пароль пользователя PostgreSQL.                                                                                                                            |
| **POSTGRES_HOST**     | Адрес сервера БД. В случае локальной разработки localhost.                                                                                                 |
| **POSTGRES_PORT**     | Порт подключения к БД (по умолчанию `5432`).                                                                                                               |
| **TASK_VERSION**      | 1                                                                                                                                                          |

---

## 3. Запуск PostgreSQL

Для работы приложения **TeamFinder** используется база данных **PostgreSQL**.
По условию задания база данных должна запускаться в контейнере Docker.

В проекте уже есть пример файла `docker-compose.yml`. 

```bash
docker compose up -d
```

#### Остановка контейнера:

```bash
docker compose down
```

## 4. Запуск Django

После заполнения `.env` и настройки базы данных можно запустить сервер разработки:

## 5. Миграции
```bash
python manage.py migrate
```
## 6. Загрузка тестовых 

```bash
python manage.py load_demo
```
Создастся 3 пользователя: demo1@example.com, demo2@example.com, demo3@example.com с одинаковым паролем demo12345 

## 7. Создание суперпользователя
```bash
python manage.py createsuperuser
```

## 8. Запуск сервера
```bash
python manage.py runserver
```
Сервер запустится по адресу: http://localhost:8000

## Проверка работоспособности
1. Откройте браузер
2. Перейдите по ссылке http://localhost:8000
3. Должен открыться список проектов или стартовая страница

___
В проекте был реализован первый вариант задания.