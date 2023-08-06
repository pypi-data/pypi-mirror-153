import json
import typing as t

import jwt
import requests
from jwt.algorithms import RSAAlgorithm
from pydantic import ValidationError

from taktile_auth.exceptions import InvalidAuthException
from taktile_auth.schemas.session import SessionState
from taktile_auth.schemas.token import TaktileIdToken
from taktile_auth.settings import settings

ALGORITHM = "RS256"


def _get_auth_server_url(env: str) -> str:
    if env == "local":
        return "http://taktile-api.local.taktile.com:8000"
    if env == "prod":
        return "https://taktile-api.taktile.com"
    return f"https://taktile-api.{env}.taktile.com"


class AuthClient:
    def __init__(
        self,
        url: str = _get_auth_server_url(settings.ENV),
    ) -> None:
        self.public_key_url = f"{url}/.well-known/jwks.json"
        self.access_token_url = f"{url}/api/v1/login/access-token"

    def get_public_key(
        self,
        *,
        key: t.Optional[str] = None,
        kid: str = "taktile-service",
    ) -> t.Any:
        jwk = (
            json.loads(key)
            if key
            else requests.get(self.public_key_url).json()
        )
        for k in jwk["keys"]:
            if k["kid"] == kid:
                return RSAAlgorithm.from_jwk(k)  # type: ignore
        raise InvalidAuthException("invalid-public-key")

    def decode_id_token(
        self,
        *,
        token: t.Optional[str] = None,
        key: t.Optional[str] = None,
        kid: str = "taktile-service",
    ) -> TaktileIdToken:
        if not token:
            raise InvalidAuthException("no-auth-provided")
        try:
            public_key = self.get_public_key(key=key, kid=kid)
            payload = jwt.decode(
                token,
                public_key,
                algorithms=[ALGORITHM],
                audience=settings.ENV,
            )
            token_data = TaktileIdToken(**payload)
        except jwt.ExpiredSignatureError:
            raise InvalidAuthException("signature-expired")
        except (jwt.PyJWTError, ValidationError):
            raise InvalidAuthException("could-not-validate")

        return token_data

    def get_access(
        self,
        *,
        session_state: SessionState,
        key: t.Optional[str] = None,
        kid: str = "taktile-service",
    ) -> t.Tuple[TaktileIdToken, SessionState]:
        if not session_state.api_key and not session_state.jwt:
            raise InvalidAuthException("no-auth-proved")
        if not session_state.jwt:
            res = requests.post(
                self.access_token_url,
                headers=session_state.to_auth_headers(),
            )
            res.raise_for_status()
            session_state.jwt = res.json()["id_token"]
        return (
            self.decode_id_token(token=session_state.jwt, key=key, kid=kid),
            session_state,
        )
