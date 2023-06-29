# Django
from django.conf import settings

# Python
import typing as t
import pickle
import abc
from cryptography.fernet import Fernet
from redis import Redis


class BaseRedisConnection(metaclass=abc.ABCMeta):
    """
    Base connection to any db.
    """

    def __init__(self, db: int, safe: bool) -> None:
        self.db = db
        self.safe = safe

    @abc.abstractmethod
    def get(self, key: str) -> t.Any:
        """
        Get some value.
        """
        pass

    @abc.abstractmethod
    def set(self, key: str, value: t.Any, eta: int = None) -> None:
        """
        Set some value.
        """
        pass


class LocalRedisConnection(BaseRedisConnection):
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


class BaseConnector(metaclass=abc.ABCMeta):
    """
    Base context manager that implements

    connection and interaction with any database.

>>> with Connector() as connection:
>>>     ...
    """

    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def __enter__(self) -> BaseRedisConnection:
        """
        Return connection with database to interract with it.
        """
        pass

    @abc.abstractmethod
    def __exit__(self, *args: t.Any) -> None:
        """
        Close connection with database.
        """
        pass


class LocalRedisConnector(BaseConnector):
    """
    Connector to redis. Set `db` value to choose redis layer.

    Set `safe` = True, if there is need to encrypt data.
    """

    def __init__(self, db: int = 0, safe: bool = False) -> None:
        # Layer of redis
        self.db = db

        # If data must be encrypted
        self.safe = safe

    def __enter__(self) -> LocalRedisConnection:
        """
        Open connection.
        """
        # Connecting to redis
        connect: LocalRedisConnection = LocalRedisConnection(db=self.db,
                                                             safe=self.safe)

        # Set attribute to close it then
        self.connect = connect

        return connect

    def __exit__(self, *args: t.Any) -> None:
        """
        Close connection.
        """
        self.connect.server.close()
