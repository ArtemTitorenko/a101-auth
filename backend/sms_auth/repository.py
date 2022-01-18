import typing
from datetime import datetime

from core.config import TIME_ZONE
from database import get_db
from fastapi import Depends
from pytz import utc
from sqlalchemy.orm import Session

from .entities import SmsVerificationDb
from .models import SmsVerification


class SmsRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def _get_by_phone_number(
        self, phone_number: str
    ) -> typing.Optional[SmsVerificationDb]:
        sms_verification = (
            self.session.query(SmsVerificationDb)
            .filter(SmsVerificationDb.phone_number == phone_number)
            .first()
        )
        return sms_verification

    def get_by_phone_number(
        self, phone_number: str
    ) -> typing.Optional[SmsVerification]:
        sms_verification = self._get_by_phone_number(phone_number)
        if not sms_verification:
            return
        return SmsVerification.from_orm(sms_verification)

    def reset_counter(self, phone_number: str) -> None:
        sms_verification = self._get_by_phone_number(phone_number)
        if not sms_verification:
            return
        sms_verification.auth_code_tries = 0
        self.session.commit()
        self.session.refresh(sms_verification)

    def increment_counter(self, sms_verification_id: int):
        sms_verification = (
            self.session.query(SmsVerificationDb)
            .filter(SmsVerificationDb.id == sms_verification_id)
            .first()
        )
        sms_verification.auth_code_tries += 1
        self.session.commit()
        self.session.refresh(sms_verification)

    def update_code(self, sms_verification_id: int, code: str):
        sms_verification: SmsVerificationDb = (
            self.session.query(SmsVerificationDb)
            .filter(SmsVerificationDb.id == sms_verification_id)
            .first()
        )
        local_time = utc.localize(datetime.now()).astimezone(TIME_ZONE)
        sms_verification.auth_code = code
        sms_verification.auth_code_time = local_time
        sms_verification.auth_code_tries = 0
        self.session.commit()
        self.session.refresh(sms_verification)

    def create(self, phone_number: str, code: str) -> typing.Optional[SmsVerification]:
        local_time = utc.localize(datetime.now()).astimezone(TIME_ZONE)
        sms_verification = SmsVerificationDb(
            phone_number=phone_number,
            auth_code=code,
            auth_code_time=local_time,
        )
        self.session.add(sms_verification)
        self.session.commit()
        return sms_verification

    def clear_auth_data(self, sms_verification_id: int) -> None:
        sms_verification: SmsVerificationDb = (
            self.session.query(SmsVerificationDb)
            .filter(SmsVerificationDb.id == sms_verification_id)
            .first()
        )
        sms_verification.auth_code = None
        sms_verification.auth_code_tries = 0
        #sms_verification.auth_code_time = None

        self.session.commit()
        self.session.refresh(sms_verification)

    def get_or_create(self, phone_number: str) -> typing.Tuple[SmsVerification, bool]:
        sms_verification: SmsVerificationDb = (
            self.session.query(SmsVerificationDb)
            .filter(SmsVerificationDb.phone_number == phone_number)
            .first()
        )
        if not sms_verification:
            return self.create(phone_number, ""), True
        return sms_verification, False
