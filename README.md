# Отчёт в Google Sheets для QRKot

## Описание проекта

Данный проект интегрируется с приложением (и расширяет функциональность изначальной версии) QRKot и автоматически создает отчёт в Google Sheets. В таблице отображаются завершённые проекты, упорядоченные по времени, за которое удалось собрать необходимые средства — начиная с самых быстрых и заканчивая теми, которые собирали средства дольше всего.

## Инструкция по развертыванию проекта

* Клонировать репозиторий: `git clone https://github.com/the-world-at-large/QRkot_spreadsheets.git`
* Создать виртуальное окружение: `python3 -m venv venv`
* Активировать виртуальное окружение: `. venv/bin/activate`
* Установить зависимости: `pip install -r requirements.txt`
* Запуск сервера: `uvicorn main:app`
* Запуск сервера с функцией автоматической перезагрузки: `uvicorn main:app --reload`
* Инициализация Alembic: `alembic init --template async alembic`
* Создание миграций: `alembic revision --autogenerate -m "migration name"`
* Применение миграций: `alembic upgrade head`
* Откат миграций: `alembic downgrade`
* Запуск тестов: `pytest`

## Шаблон наполнения файла .env
#### (также есть файл для примера - .env.example)
```
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
FIRST_SUPERUSER_EMAIL=admin@ad.ru
FIRST_SUPERUSER_PASSWORD=111111
TYPE=service_account
PROJECT_ID=mystic-span-375418
PRIVATE_KEY_ID=41c11b704ba84e7ffe65eb71b2576175cc4a4f66
CLIENT_EMAIL=foxygen@mystic-span-375418.iam.gserviceaccount.com
CLIENT_ID=101121506231304671504
AUTH_URI=https://accounts.google.com/o/oauth2/auth
TOKEN_URI=https://oauth2.googleapis.com/token
AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/foxygen%40mystic-span-375418.iam.gserviceaccount.com
EMAIL=your_gmail@gmail.com
```

## Системные требования

* Python 3.7
* FastAPI 0.7.0
* Совместимость с Linux, Windows и macOS

# Лицензия

Этот проект лицензирован по лицензии MIT. См. файл LICENSE для получения дополнительной информации.

# Автор

the-world-at-large
