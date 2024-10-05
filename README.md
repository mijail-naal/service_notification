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


<br>


### Запуск celery в Django admin-panel container

```Bash
sudo docker exec -it django_api sh -c "celery -A config worker -l info"
```

<br> 


### Запуск celery в Notification Worker container

```Bash
sudo docker exec -it worker_01 sh -c "celery -A deliver worker -l info"
```

<br> 
