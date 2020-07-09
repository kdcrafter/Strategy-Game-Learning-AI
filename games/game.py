from abc import ABC, abstractmethod, abstractproperty

class Game(ABC):
    @abstractmethod
    def __init__(self, current_player=1, board=None):
        super().__init__()

    @abstractmethod
    def setup(self, current_player=1, board=None):
        pass

    @abstractmethod
    def get_valid_actions(self):
        pass

    @abstractmethod
    def get_copy(self):
        pass

    @abstractmethod
    def get_result(self):
        pass

    @abstractmethod
    def apply(self, action):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractproperty
    def current_player(self):
        pass

    @abstractproperty
    def board(self):
        pass