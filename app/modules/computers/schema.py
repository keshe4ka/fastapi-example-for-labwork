from pydantic import BaseModel

from app.modules.users.schema import UserRead


class ComputerRead(BaseModel):
    id: int = None
    model: str
    user: UserRead = None
    error: str = None


class ComputerCreate(BaseModel):
    model: str
    user_id: int
