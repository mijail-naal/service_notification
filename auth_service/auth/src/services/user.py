from functools import lru_cache
from http import HTTPStatus

from fastapi import Depends, HTTPException
from async_fastapi_jwt_auth import AuthJWT

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select
from redis.asyncio import Redis

from db.redis import get_redis
from models.entity import User
from schemas.user import (
    UserInDB,
    UsernameLogin,
    UserEmailLogin,
    UserAccess,
    Data
)
from schemas.jwt_settings import JTWSettings


class UserService:
    def __init__(self, cache: Redis) -> None:
        self.cache = cache

    async def user_validation(self, credentials: UsernameLogin, db: AsyncSession) -> User | None:
        query = await db.execute(select(User).where(User.login == credentials.username))
        user = query.scalars().first()
        return user

    async def user_email_validation(self, credentials: UserEmailLogin, db: AsyncSession) -> User | None:
        query = await db.execute(select(User).where(User.email == credentials.email))
        user = query.scalars().first()
        return user

    async def create_user_tokens(self, credentials: UsernameLogin, authorize: AuthJWT) -> UserAccess:
        access_token = await authorize.create_access_token(subject=credentials.username)
        refresh_token = await authorize.create_refresh_token(subject=credentials.username)
        return UserAccess(access_token=access_token, refresh_token=refresh_token)

    async def create_user_tokens_with_email(self, credentials: UserEmailLogin, authorize: AuthJWT) -> UserAccess:
        access_token = await authorize.create_access_token(subject=credentials.email)
        refresh_token = await authorize.create_refresh_token(subject=credentials.email)
        return UserAccess(access_token=access_token, refresh_token=refresh_token)

    async def access_revoke(self, authorize: AuthJWT, jtw_settings: JTWSettings):
        await authorize.jwt_required()
        access_jti = (await authorize.get_raw_jwt())['jti']
        await self.cache.setex(access_jti, jtw_settings.access_expires, "true")

    async def refresh_revoke(self, authorize: AuthJWT, jtw_settings: JTWSettings):
        await authorize.jwt_refresh_token_required()
        refresh_jti = (await authorize.get_raw_jwt())['jti']
        await self.cache.setex(refresh_jti, jtw_settings.refresh_expires, "true")

    async def refresh_token(self, tokens: UserAccess, authorize: AuthJWT) -> dict:
        current_user = (await authorize.get_raw_jwt(encoded_token=tokens.refresh_token))['sub']
        new_access_token = await authorize.create_access_token(subject=current_user)
        return {"access_token": new_access_token}

    async def get_user(self, db: AsyncSession, authorize: AuthJWT) -> User | None:
        current_user = (await authorize.get_raw_jwt())['sub']
        db_user = await db.execute(select(User).where(User.login == current_user))
        return db_user.scalars().first()
    
    async def get_user_by_id(self, db: AsyncSession, data: Data) -> User | None:
        db_user = await db.execute(select(User).where(User.id == data.id))
        if not db_user:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail=f'User whit id {data.id} doesn\'t exists'
            )
        return db_user.scalars().first()

    async def get_all_users(self, db: AsyncSession) -> list[UserInDB]:
        query = await db.execute(select(User))
        users = query.scalars().all()
        return users


@lru_cache()
def get_user_service(
        cache: Redis = Depends(get_redis)
) -> UserService:
    return UserService(cache)
