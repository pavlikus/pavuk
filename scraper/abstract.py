from abc import ABC, abstractmethod


class AbstractDB(ABC):

    @abstractmethod
    def init_connection(self):
        raise NotImplementedError

    @abstractmethod
    def get_urls(self):
        raise NotImplementedError
