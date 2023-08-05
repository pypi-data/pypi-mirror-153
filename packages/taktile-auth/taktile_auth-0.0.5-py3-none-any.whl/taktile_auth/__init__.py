"""
Taktile Auth
"""
import pkg_resources

__version__ = pkg_resources.get_distribution(
    __name__.split(".", maxsplit=1)[0]
).version

from taktile_auth.client import AuthClient  # noqa: 401
from taktile_auth.exceptions import (  # noqa: 401
    InsufficientRightsException,
    InvalidAuthException,
    TaktileAuthException,
)
from taktile_auth.schemas.session import SessionState  # noqa: 401
from taktile_auth.schemas.token import TaktileIdToken  # noqa: 401
