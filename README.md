# Управление платежными запросами

## Описание проекта

Этот проект представляет собой веб-приложение, разработанное на базе Django, которое обеспечивает удобное управление платежными запросами. В основе его функциональности лежит возможность создания, просмотра, редактирования и удаления платежных запросов, а также управления пользователями и реквизитами оплаты.

## Функциональность

### Платежные запросы

- Создание новых платежных запросов с указанием суммы и статуса.
- Просмотр списка всех платежных запросов с возможностью фильтрации и поиска.
- Подробный просмотр каждого платежного запроса с возможностью редактирования и удаления.
- Управление статусом платежных запросов: отметка как "Ожидающий", "Оплаченный" или "Отмененный".

### Управление пользователями

- Создание новых пользователей с указанием электронной почты, телефона и страны.
- Просмотр списка всех пользователей с возможностью фильтрации и поиска.
- Подробный просмотр каждого пользователя с возможностью редактирования и удаления.

### Реквизиты оплаты

- Добавление новых реквизитов оплаты с указанием типа платежа, владельца, номера телефона и ограничения.
- Просмотр списка всех реквизитов оплаты с возможностью фильтрации и поиска.
- Подробный просмотр каждого реквизита оплаты с возможностью редактирования и удаления.

## Установка

Чтобы установить и запустить проект локально, выполните следующие шаги:

```bash
git clone https://github.com/Igorek95/paymentverification.git
cd paymentverification
python -m venv venv
# Для Windows
venv\Scripts\activate
# Для macOS и Linux
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py csu
python manage.py runserver