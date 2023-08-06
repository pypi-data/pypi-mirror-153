from jupyterhub import handlers
from tornado import web


class NeptuneLoginHandler(handlers.BaseHandler):
    """Custom Jupyter hub auto-login handler.

    Ref: https://github.com/jupyterhub/jupyterhub/blob/master/jupyterhub/handlers/login.py#L124
    """

    async def get(self) -> None:
        self.statsd.incr("login.request")

        user = self.current_user
        if user:
            # Set a new login cookie (possibly cleared or incorrect)
            self.set_login_cookie(user)
        else:
            # Auto-login with auth info in the request
            user = await self.login_user()
            if user is None:
                raise web.HTTPError(403)

        self.redirect(self.get_next_url(user))
