# Проектная работа 10 спринта

### [Notifications Sprint 1](https://github.com/mijail-naal/notifications_sprint_1)


[Приглашение](https://github.com/mijail-naal/notifications_sprint_1/invitations)


<br>


## Notifications Service


### Развертывание
#####  *notifications_sprint_1/docker-compose.yml*

```Bash
docker compose up --build -d
```

<br>


### Ссылки

|         service    | link
| -------------------|----------------------------------
| admim-panel        | http://localhost:8000/admin
| notification API   | http://localhost:8001/api/openapi
| RabbitMQ           | http://127.0.0.1:15672/
| MailHog            | http://0.0.0.0:8025/


<br>



## Отправка уведомления из Admin panel


### Запуск celery в Django admin-panel container

```Bash
sudo docker exec -it django_api sh -c "celery -A config worker -l info"
```

<br><br>

## Отправка уведомления из API


### После запуска Auth_service выполнять следующие команды


### Миграции

```bash
  docker exec -it auth sh -c "alembic upgrade head"
```

### Создание Роли

```bash
  docker exec -it auth sh -c "python create_roles.py"
```

### Создание Провайдеры

```bash
  docker exec -it auth sh -c "python create_providers.py"
```

### Создание суперпользователя

```bash
  docker exec -it auth sh -c "python create_superuser.py admin 12345"
```

### Создание фейк пользователи

```bash
  docker exec -it auth sh -c "python create_users.py"
```


### Запуск celery в Notification Worker container

```Bash
sudo docker exec -it worker_01 sh -c "celery -A deliver worker -l info"
```

<br><br>


Пример данных
```
{
  "users": [
    "acdbaacb-a5da-4724-ba3e-e5fd309fac80"
  ],
  "template": "new_registration",
  "event": "new_registration",
  "content": {}
}
```
