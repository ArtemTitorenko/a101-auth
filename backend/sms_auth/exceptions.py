class SmsAuthException(Exception):
    def __init__(self, message: str = ""):
        self.message = message


class VerificationTimeoutError(SmsAuthException):
    pass


class WrongAuthCodeError(SmsAuthException):
    pass


class MaxTriesError(SmsAuthException):
    pass


class PhoneNotExists(SmsAuthException):
    pass
