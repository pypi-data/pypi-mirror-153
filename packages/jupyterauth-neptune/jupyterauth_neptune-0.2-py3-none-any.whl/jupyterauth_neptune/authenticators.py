from typing import List, Optional, Tuple, TypedDict

from jupyterhub import auth, handlers, utils
from tornado import gen, web
from traitlets import Unicode

from noos_pyk.clients import http

from .clients import NeptuneClient
from .handlers import NeptuneLoginHandler


__all__ = ["NeptuneBasicAuthenticator", "NeptuneJWTAuthenticator"]


UrlHandler = Tuple[str, handlers.BaseHandler]


class UserInfo(TypedDict):
    name: str
    admin: Optional[bool]


class NeptuneAuthenticator(auth.Authenticator):
    """Auto-login Jupyterhub Authenticator.

    Ref: https://github.com/jupyterhub/jupyterhub/blob/master/jupyterhub/auth.py
    """

    login_handler = NeptuneLoginHandler
    login_service = "Neptune Gateway"

    auth_path = "/auto_login"

    # Register a custom handler and its URL
    def login_url(self, base_url: str) -> str:
        return utils.url_path_join(base_url, self.auth_path)

    def get_handlers(self, *args) -> List[UrlHandler]:
        # Combine a raw-string for regex with a f-string for interpolation
        return [(rf"{self.auth_path}", self.login_handler)]

    # Implement authenticator's main co-routine
    @gen.coroutine
    def authenticate(self, handler: web.RequestHandler, *args) -> Optional[UserInfo]:
        raise NotImplementedError


class NeptuneBasicAuthenticator(NeptuneAuthenticator):
    """Remote user Jupyterhub Authenticator.

    Ref: https://github.com/jupyterhub/jupyterhub/blob/master/jupyterhub/auth.py
    """

    auth_header_name = Unicode(
        config=True,
        default_value="X-Forwarded-Auth",
        help="The HTTP header to inspect from the forwarded request.",
    )

    @gen.coroutine
    def authenticate(self, handler: web.RequestHandler, *args) -> Optional[UserInfo]:
        header = handler.request.headers.get(self.auth_header_name)
        if not header:
            return None

        return {
            "name": header,
            "admin": None,
        }


class NeptuneJWTAuthenticator(NeptuneAuthenticator):
    """Remote user JWT-based Jupyterhub Authenticator.

    Ref: https://github.com/jupyterhub/jupyterhub/blob/master/jupyterhub/auth.py
    """

    # Neptune authentication
    auth_header_name = Unicode(
        config=True,
        default_value="X-Forwarded-Auth",
        help="The HTTP header to inspect from the forwarded request.",
    )
    auth_header_type = Unicode(
        config=True,
        default_value="Bearer",
        help="The type of HTTP header to be inspected.",
    )
    auth_server_url = Unicode(
        config=True,
        default_value="http://api.neptune-gateway/",
        help="The URL for the Neptune authentication server.",
    )

    # JWT settings
    name_claim_field = Unicode(
        config=True,
        default_value="email",
        help="The decoded claim field that contains the user name.",
    )
    admin_claim_field = Unicode(
        config=True,
        default_value="is_superuser",
        help="The decoded claim field that defines whether a user is an admin.",
    )

    @gen.coroutine
    def authenticate(self, handler: web.RequestHandler, *args) -> Optional[UserInfo]:
        """Authenticate the request and return a UserInfo dict."""
        header = handler.request.headers.get(self.auth_header_name)
        if not header:
            return None

        token = self._get_token(header)
        return self._get_userinfo(token)

    # Helpers:
    def _get_token(self, header: str) -> str:
        """Extract a token from the given header value."""
        parts = header.split()

        if len(parts) != 2:
            raise web.HTTPError(401, "Invalid authorization header.")

        if parts[0] != self.auth_header_type:
            raise web.HTTPError(401, "Invalid authorization header type.")

        return parts[1]

    def _get_userinfo(self, token: str) -> UserInfo:
        """Attempt to find and return user infos from the given token."""
        client = NeptuneClient(base_url=self.auth_server_url)
        client.set_auth_header(token)

        try:
            claims = client.whoami()
        except http.HTTPError:
            raise web.HTTPError(401, "Invalid decoded JWT.")

        name = claims.get(self.name_claim_field)
        if not name:
            raise web.HTTPError(401, "Missing name claim field.")

        return {
            "name": name,
            "admin": claims.get(self.admin_claim_field),
        }
