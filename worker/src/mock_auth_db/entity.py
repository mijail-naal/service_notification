import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from .postgres import Base


class User(Base):
    __tablename__ = 'mock_auth'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    username = Column(String, unique=True, nullable=False)
    email = Column(String(255), unique=True)

    def __repr__(self) -> str:
        return f'<User {self.username}>'
