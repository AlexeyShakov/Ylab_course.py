from fastapi import APIRouter, Depends
from src.api.v1.schemas import UserSignUp, UserSignIn, Token
from src.services import (UserService, get_user_service,
                                        get_current_user, get_token)
from src.models import User

router = APIRouter()

@router.post(
    path="/signup",
    response_model=str,
    summary="Регистрация",
    tags=["auth"],
)
def sign_up(
        input_data: UserSignUp,
        user_service: UserService = Depends(get_user_service),
) -> str:
    action = user_service.sign_up(input_data)
    return action


@router.post(
    path="/login",
    response_model=Token,
    summary="Вход на сайт",
    tags=["auth"],
)
def sign_in(
        input_data: UserSignIn,
        user_service: UserService = Depends(get_user_service),
) -> Token:
    action = user_service.sign_in(input_data)
    return action


@router.post(
    path="/refresh",
    response_model=Token,
    summary="Обновление токенов",
    tags=["auth"]

)
def refresh_token(
        refresh: str = Depends(get_token),
        user_service: UserService = Depends(get_user_service),
) -> Token:
    action = user_service.refresh_token(refresh)
    return action


@router.post(
    path="/logout_all",
    summary="Выход со всех устройств",
    tags=["auth"],
)
def logout_all(
    user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    user_service.logout_all(user)
    return {'msg': 'You have been logged out from all devices'}


@router.post(
    path="/logout",
    response_model=str,
    summary="Выход с одного устройства",
    tags=["auth"]
)
def logout(
        user: User = Depends(get_current_user),
        access_token: str = Depends(get_token),
        user_service: UserService = Depends(get_user_service),
) -> str:
    action = user_service.log_out(user, access_token)
    return action

