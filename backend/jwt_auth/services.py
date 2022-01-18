import typing

from fastapi import Depends

from .base import JwtAuth as AuthJWT


class JwtAuthService:
    def __init__(self, auth: AuthJWT = Depends(AuthJWT)):
        self.auth = auth
        self.auth._token = auth._request.cookies.get("access_token_cookie")

    def authenticate(
        self,
        subject: typing.Union[str, int] = None,
        user_claim: typing.Optional[dict] = None,
    ) -> None:
        if not subject and not user_claim:
            return
        subject = subject if subject else self.auth.get_jwt_subject()
        user_claim = user_claim if user_claim else {}
        access_token, refresh_token = self.create_tokens(subject, user_claim)
        self.set_tokens(access_token, refresh_token)

    def create_tokens(
        self,
        subject: typing.Union[str, int],
        user_claim: typing.Optional[dict] = None,
    ) -> typing.Tuple[str, str]:
        user_claim = user_claim if user_claim else {}
        access_token = self.auth.create_access_token(
            subject=subject, user_claims=user_claim
        )
        refresh_token = self.auth.create_refresh_token(
            subject=subject, user_claims=user_claim
        )
        return access_token, refresh_token

    def set_tokens(
        self, access_token: str, refresh_token: typing.Optional[str] = None
    ) -> None:
        self.auth.set_access_cookies(access_token)
        if refresh_token:
            self.auth.set_refresh_cookies(refresh_token)

    def refresh(self):
        self.auth.jwt_refresh_token_required()
        access_token = self.auth.create_access_token(
            subject=self.auth.get_jwt_subject(),
        )
        self.set_tokens(access_token)

    def clear_tokens(self):
        self.auth.jwt_required()
        self.auth.unset_jwt_cookies()

    def get_user_claim_value(self, key: str) -> typing.Optional[typing.Union[str, int]]:
        return self.auth.get_raw_jwt().get(key)
