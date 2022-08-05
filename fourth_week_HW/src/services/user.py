from functools import lru_cache
from fastapi import Depends, HTTPException, Security
from redis import Redis
from src.db import (AbstractCache, get_cache, get_session,
                                  get_blocked_access_tokens, get_active_refresh_tokens)
from src.services import ServiceMixin
from src.api.v1.schemas import UserSignIn, UserSignUp, Token, UserInf
from src.models import User
from datetime import datetime
from sqlmodel import Session
import bcrypt  # для хэширования паролей
import jwt
from src.core.config import JWT_ALGORITHM, JWT_SECRET_KEY, JWT_ACCESS_EXP, JWT_REFRESH_EXP
import uuid
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


__all__ = ("UserService", "get_user_service", "get_current_user", "get_token")

# Для получения токенов из запроса
security = HTTPBearer()


class UserService(ServiceMixin):

    def __init__(self, cache: AbstractCache, session: Session,
                 blocked_access: Redis, active_refresh: Redis):
        super().__init__(cache, session)
        self.cache = cache
        self.session = session
        self.blocked_access = blocked_access
        self.active_refresh = active_refresh

    def sign_up(self, user: UserSignUp) -> str:
        # Проверяем, что данного юзера нет в базе
        if self.session.query(User).filter(User.email == user.email).first() is None:
            # Хэшируем пароль
            hashed_pass = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
            # Добавляем юзера в базу
            new_user = User(name=user.username, email=user.email, hashed_password=hashed_pass,
                            created_at=datetime.now())
            self.session.add(new_user)
            self.session.commit()
            self.session.refresh(new_user)
            return f"Пользователь {user.username} добавлен в базу"
        else:
            raise HTTPException(status_code=403,
                                detail=f"Пользователь с таким email - {user.email} уже существует!")

    def sign_in(self, user: UserSignIn) -> Token:
        # Получаем данные пользователя по эмэйлу
        user_from_db = self.session.query(User).filter(User.name == user.username).first()
        # Вытаскиваем зашифрованный пароль
        pass_from_db = user_from_db.hashed_password
        # Проверяем, что введеный пароль совпадает с зашифрованным паролем из базы
        # Так как в базе зашифрованные пароли хранятся строками, а не байтами, мы должны их
        # превратить в байты
        if bcrypt.hashpw(user.password.encode(),
                         pass_from_db.encode()) == pass_from_db.encode():
            return self.getting_tokens(user_from_db)
        else:
            raise HTTPException(status_code=401, detail="Неверный пароль")

    def getting_tokens(self, user: User):
        created_time = datetime.now().timestamp()
        refresh_uuid = str(uuid.uuid4())
        payload_access = {
            "user_id": user.id,
            "created_time": created_time,
            "exp_time": created_time + JWT_ACCESS_EXP,
            "access_uuid": str(uuid.uuid4()),
            "refresh_uuid": refresh_uuid,
            "user_email": user.email,
            "user_name": user.name
        }
        jwt_access_token = jwt.encode(payload_access, JWT_SECRET_KEY, JWT_ALGORITHM)
        payload_refresh = {
            "user_id": user.id,
            "created_time": created_time,
            "exp_time": created_time + JWT_REFRESH_EXP,
            "refresh_uuid": refresh_uuid,
            "user_email": user.email,
            "user_name": user.name
        }
        jwt_refresh_token = jwt.encode(payload_refresh, JWT_SECRET_KEY, JWT_ALGORITHM)
        # Добавляем рефреш токен в базу к активным токенам
        self.active_refresh.rpush(str(payload_refresh["user_id"]), payload_refresh["refresh_uuid"])
        return Token(access_token=jwt_access_token, refresh_token=jwt_refresh_token)

    def refresh_token(self, refresh_token: str) -> Token:
        decoded_token = jwt.decode(refresh_token, JWT_SECRET_KEY, [JWT_ALGORITHM])
        user_id = decoded_token.get("user_id")
        refresh_uuid = decoded_token.get("refresh_uuid")
        # Достанем список активных рефреш токенов из базы
        active_refresh = self.active_refresh.lrange(str(user_id), 0, -1)
        if refresh_uuid in active_refresh:
            # Удаляем данный uuid так как он перестает быть активным
            self.active_refresh.lrem(str(user_id), 0, refresh_uuid)
            user_from_db = self.session.query(User).filter(User.id == user_id).first()
            return self.getting_tokens(user_from_db)
        raise HTTPException(status_code=401, detail="Токен неверный или он просрочен")

    def update_user(self, user: User, user_update: UserInf) -> User:
        if user_update.email is not None:
            user.email = user_update.email
        if user_update.username is not None:
            user.name = user_update.username
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def log_out(self, user: User, access_token: str) -> str:
        # Добавим access токен в список неактивных
        decoded_access = jwt.decode(access_token, JWT_SECRET_KEY, [JWT_ALGORITHM])
        user_id = decoded_access.get("user_id")
        access_uuid = decoded_access.get("access_uuid")
        self.blocked_access.rpush(str(user_id), access_uuid)
        # Удалим refresh токен из списка активных
        refresh_uuid = decoded_access.get("refresh_uuid")
        # decoded_refresh = jwt.decode(refresh_token, JWT_SECRET_KEY, [JWT_ALGORITHM])
        # refresh_uuid = decoded_refresh.get("refresh_uuid")
        self.active_refresh.lrem(str(user_id), 0, refresh_uuid)
        return f"Вы вышли с данного устройства"

    def logout_all(self, user):
        self.active_refresh.delete(str(user.id))


def get_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    return credentials.credentials


def get_current_user(
    token: str = Depends(get_token),
    session: Session = Depends(get_session),
    blocked_access_tokens: Redis = Depends(get_blocked_access_tokens),
):
    decode_token = jwt.decode(
        token,
        JWT_SECRET_KEY,
        algorithms=[JWT_ALGORITHM]
    )
    access_uuid = decode_token["access_uuid"]
    user_id = decode_token.get('user_id')
    blocked_access = blocked_access_tokens.lrange(str(user_id), 0, -1)
    if access_uuid in blocked_access:
        raise HTTPException(status_code=401, detail="Токен неверный или он просрочен")
    # if blocked_access_tokens.exists(decode_token.get('access_uuid')):
    #     raise HTTPException(401)
    user = session.query(User).filter(
        User.id == user_id
    ).first()
    if not user:
        raise HTTPException(status_code=401, detail="Такого юзера не существует")
    return user

@lru_cache()
def get_user_service(
    cache: AbstractCache = Depends(get_cache),
    session: Session = Depends(get_session),
    blocked_access: Redis = Depends(get_blocked_access_tokens),
    active_refresh: Redis = Depends(get_active_refresh_tokens),
) -> UserService:
    return UserService(
        cache=cache,
        session=session,
        blocked_access=blocked_access,
        active_refresh=active_refresh
    )






