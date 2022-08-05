from pydantic import BaseModel
from typing import Optional

__all__ = (
    "UserBase",
    "UserSignUp",
    "UserSignIn",
    "UserInf"
)


class UserBase(BaseModel):
    username: str


class UserSignIn(UserBase):
    password: str


class UserSignUp(UserSignIn):
    email: str


# Для обновления данных пользователя. Здесь повторяются все столбцы из базы данных
# кроме id и пароля
class UserInf(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None


