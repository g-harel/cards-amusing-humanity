from abc import ABC, abstractmethod


class Storage(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get(self, key):
        """ Get data using key """
        pass

    @abstractmethod
    def set(self, key, data):
        """ Set an entry """
        pass

    @abstractmethod
    def exists(self, key):
        """ Does the key exists """ 
        pass
