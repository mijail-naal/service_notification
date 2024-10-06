import typer

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.entity import User
from core.config import pg, settings


DATABASE_URL = f'postgresql+psycopg2://{pg.user}:{pg.password}@{pg.host}:{pg.port}/{pg.db}'


engine = create_engine(DATABASE_URL, echo=settings.echo_var, future=True)
session_maker = sessionmaker(
    engine, expire_on_commit=False
)
session = session_maker()


def create_users():
    users = [
        ['Jane', "acdbaacb-a5da-4724-ba3e-e5fd309fac80"],
        ['John', "c3242d9b-4ff7-494e-9cc4-4fc9842c0ba1"],
        ['Foo', "04b030ed-71aa-4184-b18e-612614460736"]
    ]

    for user, user_id in users:
        data = {
            'login': user,
            'password': '12345',
            'email': f'{user}@mail.com',
            'first_name': user,
            'last_name': 'Doe'
        }
        obj = User(
            login=data['login'],
            password=data['password'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )

        obj.id = user_id
        
        session.add(obj)
        session.commit()
    typer.echo('Users created successfully')


if __name__ == '__main__':
    typer.run(create_users)
