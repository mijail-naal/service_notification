from pydantic import BaseModel, EmailStr


class UserModel(BaseModel):
    id: int
    username: str
    email: EmailStr


class FakeUserJohn(BaseModel):
    id: str = 'be637291-ecc8-4ece-9f0a-270d7217ca9e'
    username: str = 'John'
    email: EmailStr = 'john@mail.com'


class FakeUserJane(BaseModel):
    id: int = '2b1d3a78-7db2-4c0c-84ba-611f4fde8ae5'
    username: str = 'Jane'
    email: EmailStr = 'john@mail.com'


john = FakeUserJohn()
jane = FakeUserJane()
