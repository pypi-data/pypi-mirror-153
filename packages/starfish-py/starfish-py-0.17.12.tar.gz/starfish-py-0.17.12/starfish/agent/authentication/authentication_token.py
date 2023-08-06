"""


    AuthenticationToken


"""

from .authentication import Authentication


class AuthenticationToken(Authentication):

    def __init__(self, token):
        super().__init__()
        self._token = token

    def is_access(self, access_data):
        if self.token and self._token == access_data:
            return True
        return False

    @property
    def token(self):
        return self._token

    @property
    def md5hash(self):
        return Authentication.calc_md5hash(self._token)
