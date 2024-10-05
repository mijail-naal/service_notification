from pydantic import BaseModel


class EmailNotification(BaseModel):
    users: list
    template: str
    event: str
    content: dict
