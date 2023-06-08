from pydantic import BaseModel


class UserRead(BaseModel):
    id: int
    name: str
    email: str


class UserUpdate(BaseModel):
    name: str
    email: str
