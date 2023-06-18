# Python
from redis import Redis
import typing as t
import pickle
from abc import (
    ABCMeta,
    abstractmethod,
)
from cryptography.fernet import Fernet

# Django
from django.conf import settings


class BaseConnection(metaclass=ABCMeta):
    """
    Base connection to any db.
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def get(self) -> t.Any:
        """
        Get some value.
        """
        pass

    @abstractmethod
    def set(self) -> None:
        """
        Set some value.
        """
        pass


class RedisConnection(BaseConnection):
    """
    Connetion to redis.
    """

    def __init__(self, db: int, safe: bool) -> None:
        assert isinstance(db, int)

        # Fernet instance to encrypt and decrypt data
        self.fernet: Fernet = Fernet(settings.FERNET_KEY)

        # Other fields
        self.host = 'localhost'
        self.port = '6379'
        self.db = db

        # Is information must be encrypted
        self.encrypt = safe

        # Connect to redis database
        self.server: Redis = Redis(host=self.host, port=self.port,
                                   db=self.db, decode_responses=False)

    def get(self, key: str) -> t.Any:
        """
        Get value from redis.
        """
        assert isinstance(key, str)

        # If value is already cached
        if value := self.server.get(key):

            # If encryption is on
            if self.encrypt is True:

                # Decrypt value
                value: t.Any = self.fernet.decrypt(value)

            # Return cached value
            return pickle.loads(value)

    def set(self, key: str, value: t.Any, eta: int = None) -> None:
        """
        Set value in redis. Set `eta` to give lifetime to the value.
        """
        assert isinstance(key, str)

        # Serializes data to bytes
        value: bytes = pickle.dumps(value)

        # If encryption is on
        if self.encrypt is True:

            # Encrypt value
            value = self.fernet.encrypt(value)

        # Set value in redis
        self.server.set(name=key, value=value, ex=eta)


class BaseConnector(metaclass=ABCMeta):
    """
    Base context manager that implements

    connection and interaction with any database.

>>> with Connector() as connection:
>>>     ...
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def __enter__(self) -> BaseConnection:
        """
        Return connection with database to interract with it.
        """
        pass

    @abstractmethod
    def __exit__(self, *args: tuple) -> None:
        """
        Close connection with database.
        """
        pass


class RedisConnector(BaseConnector):
    """
    Connector to redis. Set `db` value to choose redis layer.

    Set `safe` = True, if there is need to encrypt data.
    """

    def __init__(self, db: int = 0, safe: bool = False) -> None:
        # Layer of redis
        self.db = db

        # If data must be encrypted
        self.safe = safe

    def __enter__(self) -> RedisConnection:
        """
        Open connection.
        """
        # Connecting to redis
        connect: RedisConnector = RedisConnection(db=self.db, safe=self.safe)

        # Set attribute to close it then
        self.connect = connect

        return connect

    def __exit__(self, *args: t.Any) -> None:
        """
        Close connection.
        """
        self.connect.server.close()
