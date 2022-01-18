from datetime import datetime, timedelta
from random import randint
from uuid import UUID

from core.config import TIME_ZONE
from fastapi import Depends
from jwt_auth.services import JwtAuthService
from pytz import utc

from users.exceptions import UserNotRegistered
from users.models import User
from users.repository import UserRepository
from users.schemas import UserCreateData

from .exceptions import *
from .models import SmsVerification
from .repository import SmsRepository
from .schemas import AuthConfirmData, AuthData, SignUpData

MAX_TRIES = 3
TIME_INTERVAL = timedelta(hours=3)
AUTH_CODE_LIVING_TIME_INTERVAL = timedelta(minutes=2)


class SmsAuthService:
    def __init__(
        self,
        sms_repo: SmsRepository = Depends(SmsRepository),
        user_repo: UserRepository = Depends(UserRepository),
        jwt_auth_service: JwtAuthService = Depends(JwtAuthService),
    ) -> None:
        self.sms_repo = sms_repo
        self.user_repo = user_repo
        self.jwt_service = jwt_auth_service

    def signup(self, signup_data: SignUpData) -> None:
        self.jwt_service.auth.jwt_required()
        user = self.user_repo.create(user_data=UserCreateData(**signup_data.dict()))
        self.jwt_service.authenticate(subject=str(user.id), user_claim=dict(is_authenticated=False))
        self.send_verification_code(user.phone_number)

    def authenticate(self, auth_data: AuthData):
        self.jwt_service.auth.jwt_required()
        user = self.user_repo.get_by_phone_number(auth_data.phone_number)
        if user is None:
            raise UserNotRegistered("Сначала нужно зарегистрироваться")
        self.send_verification_code(user.phone_number)
        self.jwt_service.authenticate(subject=str(user.id), user_claim=dict(is_authenticated=False))

    def send_verification_code(self, phone_number: str) -> None:
        sms_verification, created = self.sms_repo.get_or_create(phone_number)
        self._check_sms_throttling(sms_verification)
        code = self._generate_verification_code()
        self.sms_repo.update_code(sms_verification.id, code)

    @staticmethod
    def _check_sms_throttling(sms_verification: SmsVerification) -> None:
        local_time = utc.localize(datetime.now()).astimezone(TIME_ZONE)
        auth_code_time = sms_verification.auth_code_time.astimezone(TIME_ZONE)
        if sms_verification.auth_code and auth_code_time > local_time - timedelta(minutes=1):
            raise MaxTriesError("Слишком много отправлений, попробуйте позже.")

    @staticmethod
    def _generate_verification_code(n: int = 4) -> str:
        random_number = str(randint(0, int("9" * n)))
        return "0" * (n - len(random_number)) + random_number

    def confirm(self, confirm_data: AuthConfirmData) -> None:
        self.jwt_service.auth.jwt_required()
        user = self.user_repo.get(UUID(self.jwt_service.auth.get_jwt_subject()))
        if user is None:
            raise UserNotRegistered("Сначала нужно зарегистрироваться")
        sms_verification = self._validate_confirm_data(user, confirm_data)
        user = self.user_repo.auth(user.id)
        self.jwt_service.authenticate(
            subject=str(user.id),
            user_claim=dict(
                anonymous_user=self.jwt_service.auth.get_jwt_subject(),
                is_authenticated=True,
            ),
        )
        self.sms_repo.clear_auth_data(sms_verification.id)

    def _validate_confirm_data(self, user: User, confirm_data: AuthConfirmData) -> SmsVerification:
        sms_verification = self.sms_repo.get_by_phone_number(user.phone_number)
        self._check_auth_code_exists(sms_verification)
        self._check_confirm_time(sms_verification)
        self._check_tries(sms_verification)
        self._check_auth_code_is_correct(confirm_data.auth_code, sms_verification)
        return sms_verification

    @staticmethod
    def _check_auth_code_exists(sms_verification: SmsVerification) -> None:
        if sms_verification.auth_code is None:
            raise VerificationTimeoutError("Отсутсвует код авторизации")

    @staticmethod
    def _check_tries(sms_verification: SmsVerification) -> None:
        if sms_verification.auth_code_tries >= MAX_TRIES:
            raise MaxTriesError("Слишком много попыток, попробуйте взять другой код")

    def _check_confirm_time(self, sms_verification: SmsVerification) -> None:
        local_time = utc.localize(datetime.now()).astimezone(TIME_ZONE)
        auth_code_time = sms_verification.auth_code_time.astimezone(TIME_ZONE)
        if (
            sms_verification.auth_code is None
            or auth_code_time < local_time - AUTH_CODE_LIVING_TIME_INTERVAL
        ):
            self.sms_repo.clear_auth_data(sms_verification.id)
            raise VerificationTimeoutError("Код авторизации устарел")

    def _check_auth_code_is_correct(
        self, user_auth_code: str, sms_verification: SmsVerification
    ) -> None:
        if sms_verification.auth_code != user_auth_code:
            self.sms_repo.increment_counter(sms_verification.id)
            raise WrongAuthCodeError("Неверный код")
