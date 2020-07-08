from abc import ABC, abstractmethod, abstractproperty

class Game(ABC):
    def __init__(self):
        super().__init__()

    @abstractproperty
    def current_player(self):
        pass

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def get_valid_actions(self):
        pass

    @abstractmethod
    def apply(self, action):
        pass

    @abstractmethod
    def get_result(self):
        pass

    @abstractmethod
    def __str__(self):
        pass