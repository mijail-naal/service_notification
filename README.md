# Notification Service

### Description

The notification service is responsible for communicating with the user via Email, mobile push notifications, and websocket in the browser. This is a frequently solved business problem in commercial development. Business performance depends on proper communication with the user.

Project content:
- GitHub actions (continuous integration)
- Admin panel with Django to create and send email notification
- Authorization service
- API to send a notification message to broker
- Worker to receive notifications and send email

<br>

### Two steps are needed to launch the project:

- *Change the file `.env.example` to `.env` and set the environment variables* 

- *Run the `docker-compose.yml` file*

<br>

*All environment variables samples are included in the `.env.sample` files.*

*Don't forget to set the environment variables before running the project!*


<br>

### Technologies used:

![Technologies used](https://skillicons.dev/icons?i=python,django,fastapi,nginx,postgres,mongo,rabbitmq,docker)  
<img width="64" alt="Celery logo" src="https://upload.wikimedia.org/wikipedia/commons/1/19/Celery_logo.png?20170817002532">


###### Python, Django, Fastapi, Nginx, PostgreSQL, MongoDB, RabbitMQ, Docker, Celery, Mailhog


<br><br>


# Run the project

### 1. Set the environment variables
```
Change all .env.sample files to .env and set the environment variables in the next locations:

- admin/.env
- auth_service/auth/env/prod/.env
- auth_service/.env
- notification/notification_api/env/prod/.env
- worker/src/.env
- ./.env
```

<br>

### 2. Run docker-compose.yml
```
$ cd service_notification/

$ sudo docker compose up --build -d
```

<br>

### 3. Run celery in the admin-panel container 
##### *To send email notification via admin panel*
```bash
sudo docker exec -it django_api sh -c "celery -A config worker -l info"
```

<br>

### 4. Run the next commnads to send email notifications via API
##### *Execute the commands after starting authorization service*

```bash
# Migrations

  docker exec -it auth sh -c "alembic upgrade head"


# Create roles

  docker exec -it auth sh -c "python create_roles.py"


# Create providers

  docker exec -it auth sh -c "python create_providers.py"


# Create superuser

  docker exec -it auth sh -c "python create_superuser.py admin 12345"


# Create fake users

  docker exec -it auth sh -c "python create_users.py"


# Start celery in notification worker container

  sudo docker exec -it worker_01 sh -c "celery -A deliver worker -l info"
```

<br>


### Local URLs

|         service    | link
| -------------------|----------------------------------
| admim-panel        | http://localhost:8000/admin
| notification API   | http://localhost:8001/api/openapi
| RabbitMQ           | http://127.0.0.1:15672/
| MailHog            | http://0.0.0.0:8025/

<br><br>

### Type of data stored in MongoDB

```bash
{
  "users": [
    "acdbaacb-a5da-4724-ba3e-e5fd309fac80"
  ],
  "template": "new_registration",
  "event": "new_registration",
  "content": {}
}
```
