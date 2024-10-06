from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.auth_jwt import AuthJWTBearer

from db.postgres import get_session
from db.redis import redis
from services.user import UserService, get_user_service
from schemas.user import (
    UserInDB,
    UsernameLogin,
    UserAccess,
    UserRoles,
    UserInDBRole,
    Data
)
from schemas.jwt_settings import JTWSettings
from schemas.auth_request import AuthRequest
from .user_auth import roles_required, get_current_user_global


router = APIRouter()
auth_dep = AuthJWTBearer()
jtw_settings = JTWSettings()


@AuthJWT.load_config
def get_config():
    return jtw_settings


@AuthJWT.token_in_denylist_loader
async def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token["jti"]
    entry = await redis.get(jti)
    return entry and entry == "true"


@router.post('/signin', response_model=UserAccess, status_code=HTTPStatus.OK)
async def login(
    credentials: UsernameLogin,
    user_service: UserService = Depends(get_user_service),
    db: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(auth_dep)
) -> UserAccess | None:
    user = await user_service.user_validation(credentials, db)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Username doesn\'t exists'
        )
    if not user.check_password(credentials.password):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Incorrect password'
        )
    tokens = await user_service.create_user_tokens(credentials, authorize)
    await authorize.set_access_cookies(tokens.access_token)
    await authorize.set_refresh_cookies(tokens.refresh_token)
    return tokens


@router.delete('/signout', status_code=HTTPStatus.OK)
async def logout(
    user_service: UserService = Depends(get_user_service),
    authorize: AuthJWT = Depends(auth_dep)
) -> dict:
    await authorize.jwt_required()
    await user_service.access_revoke(authorize, jtw_settings)
    await user_service.refresh_revoke(authorize, jtw_settings)
    await authorize.unset_jwt_cookies()
    return {"detail": "Logged out successfully"}


@router.post('/refresh', status_code=HTTPStatus.OK)
async def refresh(
    authorize: AuthJWT = Depends(auth_dep)
) -> dict:
    await authorize.jwt_refresh_token_required()

    current_user = await authorize.get_jwt_subject()
    new_access_token = await authorize.create_access_token(subject=current_user)
    await authorize.set_access_cookies(new_access_token)
    return {"access_token": new_access_token}


@router.post('/user',response_model=UserInDB, status_code=HTTPStatus.OK)
#@roles_required(roles_list=[UserRoles().admin, UserRoles().superuser])
async def create_user(
    data: Data,
    user_service: UserService = Depends(get_user_service),
    db: AsyncSession = Depends(get_session),
    #authorize: AuthJWT = Depends(auth_dep)
) -> UserInDB:
    user = await user_service.get_user_by_id(db, data)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=f'User whit id {data.id} doesn\'t exists'
        )
    return user


@router.get('/users', status_code=HTTPStatus.OK)
@roles_required(roles_list=[UserRoles().admin, UserRoles().superuser])
async def get_users(
    *,
    request: AuthRequest,
    permission: AuthJWTBearer = Depends(get_current_user_global),
    user_service: UserService = Depends(get_user_service),
    db: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(auth_dep)
) -> list[UserInDBRole]:
    await authorize.jwt_required()

    return await user_service.get_all_users(db)
