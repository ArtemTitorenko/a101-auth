from uuid import uuid4

from fastapi import APIRouter, Depends

from .services import JwtAuthService

router = APIRouter()


@router.post("/token")
async def login(jwt_service: JwtAuthService = Depends(JwtAuthService)) -> dict:
    jwt_service.authenticate(str(uuid4()))
    return {"detail": "Successfully login"}


@router.post("/refresh")
async def refresh(jwt_service: JwtAuthService = Depends(JwtAuthService)) -> dict:
    jwt_service.refresh()
    return {"detail": "The token has been refresh"}


@router.delete("/logout")
async def logout(jwt_service: JwtAuthService = Depends(JwtAuthService)) -> dict:
    jwt_service.clear_tokens()
    return {"detail": "Successfully logout"}
