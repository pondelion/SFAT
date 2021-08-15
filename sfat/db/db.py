from abc import ABCMeta, abstractmethod
from enum import Enum


class DBType(Enum):
    AMAZON_RDS = 'amazon_rds'
    DYNAMO_DB = 'dynamo_db'


class DB(metaclass=ABCMeta):

    @abstractmethod
    def save(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get_list(self, **kwargs):
        raise NotImplementedError

    @property
    @abstractmethod
    def type(self) -> DBType:
        raise NotImplementedError
