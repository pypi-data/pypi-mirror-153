"""


    AuthenticationBasic


"""

from .authentication import Authentication


class AuthenticationBasic(Authentication):

    def __init__(self, username, password):
        super().__init__()
        self._username = username
        self._password = password

    def is_access(self, access_data):
        if self._username and self._password and self._password == access_data:
            return True
        return False

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def md5hash(self):
        return Authentication.calc_md5hash(self._username)
