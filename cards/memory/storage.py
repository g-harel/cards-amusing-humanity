from abc import ABC, abstractmethod


class Storage(ABC):

    @abstractmethod
    def answers_for_deck(self, deck):
        pass

    @abstractmethod
    def questions_for_deck(self, deck):
        pass
