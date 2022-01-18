class BaseUserException(Exception):
    def __init__(self, message: str = ""):
        self.message = message


class UserAlreadyExistsError(BaseUserException):
    pass


class UserNotRegistered(BaseUserException):
    pass
