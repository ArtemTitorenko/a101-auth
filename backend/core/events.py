from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException
from phonenumbers.phonenumberutil import NumberParseException
from sms_auth.exceptions import SmsAuthException
from users.exceptions import BaseUserException
from sqlalchemy.orm.exc import NoResultFound


def no_result_found_handler(request: Request, exc: NoResultFound):
    return JSONResponse(status_code=404, content={"detail": "No result found"})


def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


def sms_auth_exception_handler(request: Request, exc: SmsAuthException):
    return JSONResponse(status_code=422, content={"detail": exc.message})


def user_exception_handler(request: Request, exc: BaseUserException):
    return JSONResponse(status_code=422, content={"detail": exc.message})
