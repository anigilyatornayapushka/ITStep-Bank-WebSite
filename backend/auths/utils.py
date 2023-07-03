# Django
from django.conf import settings

# Python
import random
import hashlib
import abc


# alphabet of generated code
alpha: str = '1234567890'


def generate_code(length: int) -> str:
    """
    Generate a random code of a certain length.

    Code contains letters and numbers.
    """
    code: str = ''
    for _ in range(length):
        code = code + random.choice(alpha)
    return code


class BaseHasher(metaclass=abc.ABCMeta):
    """
    Base hasher.
    """

    @abc.abstractmethod
    def hash(self, string: str) -> str:
        """
        Hash string.
        """
        pass


class Sha256Hasher(BaseHasher):
    """
    Hasher using sha256.
    """

    def hash(self, string: str) -> str:
        # Create salt
        salt = settings.SECRET_KEY.encode('utf-8')

        # Hash string
        hash_object = hashlib.sha256()
        token_with_salt = string.encode('utf-8') + salt
        hash_object.update(token_with_salt)
        hash_result = hash_object.hexdigest()

        return hash_result
