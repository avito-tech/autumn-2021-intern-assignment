# Микросервис для работы с балансом пользователей.

## Приложение "USERS":
Позволяет производить регистрацию пользователей, аутентификацию с помощью токена, при регистрации пользователя, автоматически создаётся кошелек. Пополнение кошелька осуществляется с помощью денежной карточки. Так же имеется возможность восстановления пароля. Перевод средств между пользователями.

## Приложение "BANKCONTROLLER":

Позволяет просмотреть все предоставленные для покупки услуги, стоимость и используемая валюта. Услугу может создать, изменить или удалить только администратор сайта. Приобрести услугу, может только авторизованный полтзователь.


---

### **Используемые технологии:**
- Python
- Django Rest Framework
- Docker
- PostgreSQL


---

### **Инфраструктура:**
- Проект работает с СУБД __PostgreSQL__.
- Для регистрации, авторизации используется библиотека __Djoser__
- Осуществляются запросы к базе данных и одновременно создаются RESTful WEB API  с помощью библиотеки __Django Rest Framework__
- Для развертывания проекта используется __Docker__

---

### Для запуска проекта:

- Клонировать репозиторий ```https://github.com/h0diush/autumn-2021-intern-assignment.git```
- Создать файл ```.env``` и заполнить его
```
SECRET_KEY='django-insecure-yab)bkl4$_l*@_u*5u&)3nb2$n6@l5i45o#fys@7&=s8g2=#_o'
DEBUG=True
ALLOWED_HOSTS=localhost 127.0.0.1 [::1]

DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=postgres-db
DB_PORT=5432

EMAIL_HOST=...
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=...
EMAIL_PORT=...
```
#### ***!ВАЖНО!*** Для работы сервиса необходим заранее установленный Docker и docker-compose
- Запустить контейнер ```docker-compose up -d --build```
- Посмотреть логи docker’a ```docker-compose logs```
- Документация API: 
>  ```
> http://localhost:8000/redoc/
> http://localhost:8000/schema/swagger-ui/
> ```
- создать суперпользователя ```docker-compose exec api python manage.py createsuperuser```
- Заполнить базу данных ```docker-compose exec api python manage.py loaddata data/service.json```


- Данные для входа администратора сайта: 
> ```
> email: admin@api.com
> password: admin
>```

- Остановить контейнер ```docker-compose down -v```

---
## Примеры запросов и ответов:

- Список пользователей ``` GET http://localhost:8000/users/```

> ```
> "count": 123,
> "next": "http://api.example.org/accounts/?page=4",
> "previous": "http://api.example.org/accounts/?page=2",
> "results": [
>     {
>         "email": "user@example.com",
>         "id": 0,
>         "first_name": "string",
>         "last_name": "string"
>         },
>     ]
> }
> ```

- Создание пользователя: ``` POST http://localhost:8000/users/```
> ```
>{
>    "email": "user@example.com",
>    "first_name": "string",
>    "last_name": "string",
>    "phone": "string",
>    "password": "string"
>}
> ```

- Создане токена ```POST http://localhost:8000/auth/token/login/```
> ```
> {
>   "password": "string",
>   "email": "string"
> }
> ```

- Профиль ```GET http://localhost:8000/users/me/```
> ```
> {
>     "email": "user@example.com",
>     "id": 0,
>     "first_name": "string",
>     "last_name": "string",
>     "phone": "string",
>     "balance": 0.00
> }
> ```

- Пополнение кошелька ```POST http://localhost:8000/create_money_card/```
> ```
>{
>    "number": "string",
>    "month": "01",
>    "year": "2021",
>    "amount": 0.00
>}
>```

- Список услуг ```GET http://localhost:8000/services/```
>```
>"count": 123,
>"next": "http://api.example.org/accounts/?page=4",
>"previous": "http://api.example.org/accounts/?page=2",
>"results": [
>        {
>            "name": "string",
>            "id": 0,
>            "description": "string",
>            "price": 0.00,
>            "currency": "USD",
>            "purchased": true
>        }
>    ]
>}
>```
- Приобретение услуги ```GET http://localhost:8000/services/{id}/shop/```

- Перевод денежных средств ```POST http://localhost:8000/users/{id}/money_trafic/```
> ```
>{
>    "amount": 0.00
>}
>```

- Список денежных транзакций ```GET http://localhost:8000/info_list_money_transfer/```
> ```
> "count": 123,
> "next": "http://api.example.org/accounts/?page=4",
> "previous": "http://api.example.org/accounts/?page=2",
> "results": [
>         {
>             "user_received": "string",
>             "amount": 0.00,
>             "date": "2019-08-24T14:15:22Z"
>         }
>     ]
> }
> ```
- Список приобретенных услуг ```GET http://localhost:8000/info_list_service/```
>```
>"count": 123,
>"next": "http://api.example.org/accounts/?page=4",
>"previous": "http://api.example.org/accounts/?page=2",
>"results": [
>        {
>            "service": {
>                "name": "string",
>                "price": 0.00
>            },
>            date": "string"
>        }
>    ]
>}
>```
- Так же добавлена фильтрация по ценам на услуги и используемой валюте. Приобретена услуга или нет. Фильтрация по дате приобретения услуги и переводе денежных средств