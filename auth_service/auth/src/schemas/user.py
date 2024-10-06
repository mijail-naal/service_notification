from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    login: str = Field(min_length=4, max_length=255)
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class UserInDB(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserInDBRole(UserInDB):
    role_id: int


class UserRoles(BaseModel):
    user: int = 1
    admin: int = 2
    superuser: int = 3


class UserEmailLogin(BaseModel):
    email: EmailStr
    password: str


class UsernameLogin(BaseModel):
    username: str
    password: str


class UserAccess(BaseModel):
    access_token: str
    refresh_token: str


class Data(BaseModel):
    id: UUID
