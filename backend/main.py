import locale

from core.config import ALLOWED_HOSTS, DEBUG
from core.events import (
    authjwt_exception_handler,
    no_result_found_handler,
    sms_auth_exception_handler,
)
from fastapi import FastAPI
from fastapi_jwt_auth.exceptions import AuthJWTException
from jwt_auth.api import router as jwt_router
from sms_auth.api import router as sms_auth_router
from sms_auth.exceptions import SmsAuthException
from users.exceptions import BaseUserException
from sqlalchemy.orm.exc import NoResultFound
from starlette.middleware.cors import CORSMiddleware

locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")


def get_application() -> FastAPI:
    application = FastAPI(title="app", debug=DEBUG)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_exception_handler(NoResultFound, no_result_found_handler)
    application.add_exception_handler(AuthJWTException, authjwt_exception_handler)
    application.add_exception_handler(SmsAuthException, sms_auth_exception_handler)
    application.add_exception_handler(BaseUserException, sms_auth_exception_handler)

    api_prefix = "/api"
    application.include_router(jwt_router, prefix=f"{api_prefix}", tags=["jwt"])
    application.include_router(
        sms_auth_router, prefix=f"{api_prefix}", tags=["sms-auth"]
    )

    return application


app = get_application()
