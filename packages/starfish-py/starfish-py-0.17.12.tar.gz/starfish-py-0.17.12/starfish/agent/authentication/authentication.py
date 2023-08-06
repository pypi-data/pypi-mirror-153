"""


    Authentication

"""
import hashlib

from abc import (
    ABC,
    abstractmethod,
    abstractproperty
)


class Authentication(ABC):

    @abstractmethod
    def is_access(self, access_data):
        return False

    @abstractproperty
    def md5hash(self):
        return None

    @staticmethod
    def calc_md5hash(text):
        return hashlib.md5(text.encode()).hexdigest()
