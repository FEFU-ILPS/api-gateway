from fastapi import APIRouter, Body
from schemas.auth import AuthRequest

router = APIRouter("/auth")


@router.get("", summary="Authenticate User", tags=["Auth"])
def athenticate_user(user_data: AuthRequest = Body()):
    """Производит аутентификацию пользователя по его имени и паролю.
    Возвращает пару refresh и acess токенов.
    """
    pass
