from fastapi import APIRouter, Depends
from src.services import UserService, get_user_service, get_current_user
from src.api.v1.schemas import UserInf
from src.models import User

router = APIRouter()

@router.get(
    path="/me",
    response_model=User,
    summary="Просмотр информации о себе",
    tags=["users"],
)
def get_user(
    user: User = Depends(get_current_user),
):
    return user


@router.patch(
    path="/me",
    response_model=User,
    summary="Обновляет информацию о себе",
    tags=["users"],
)
def update_user(
    user_update: UserInf,
    user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    return user_service.update_user(user, user_update)

