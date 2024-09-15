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
APP_TITLE=QRKot
APP_DESCRIPTION=Благотворительный фонд поддержки котов
DATABASE_URL=sqlite+aiosqlite:///qr_kot.db
SECRET='WDYWFM'
FIRST_SUPERUSER_EMAIL=userr@example.com
FIRST_SUPERUSER_PASSWORD=userpassword
TYPE=service_account
PROJECT_ID=nice-root-430207-q1
PRIVATE_KEY_ID=8d7d5659782af5b345800ee1c5de094cfcecb588
PRIVATE_KEY= ...
EMAIL_USER=lolkalalalka@gmail.com
CLIENT_EMAIL=i0ne1y-w@nice-root-430207-q1.iam.gserviceaccount.com
CLIENT_ID=112994020176159352479
AUTH_URI=https://accounts.google.com/o/oauth2/auth
TOKEN_URI=https://oauth2.googleapis.com/token
AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/i0ne1y-w%40nice-root-430207-q1.iam.gserviceaccount.com
UNIVERSE_DOMAIN=googleapis.com

```

## Системные требования

* Python 3.7
* FastAPI 0.7.0
* Совместимость с Linux, Windows и macOS

# Лицензия

Этот проект лицензирован по лицензии MIT. См. файл LICENSE для получения дополнительной информации.

# Автор
the-world-at-large
