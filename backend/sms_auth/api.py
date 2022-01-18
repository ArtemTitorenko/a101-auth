from fastapi import Depends
from fastapi.routing import APIRouter
from jwt_auth.services import JwtAuthService
from sms_auth.services import SmsAuthService

from .schemas import AuthConfirmData, AuthData, SignUpData

router = APIRouter()


@router.post("/signup")
async def signup(
    signup_data: SignUpData, sms_service: SmsAuthService = Depends(SmsAuthService)
) -> dict:
    sms_service.signup(signup_data)
    return {"detail": "Данные получены"}


@router.post("/sms-auth")
async def create_sms_auth(
    auth_data: AuthData,
    sms_service: SmsAuthService = Depends(SmsAuthService),
) -> dict:
    sms_service.authenticate(auth_data)
    return {"detail": "Код отправлен"}


@router.patch("/sms-auth")
async def update_sms_auth(
    auth_data: AuthConfirmData,
    sms_service: SmsAuthService = Depends(SmsAuthService),
) -> dict:
    sms_service.confirm(auth_data)
    return {"detail": "Подтверждение прошло успешно"}
