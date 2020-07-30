from abc import ABC, abstractmethod, abstractproperty
from copy import deepcopy
import numpy as np

class Game(ABC):
    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def actions(self):
        pass

    @abstractmethod
    def valid_actions(self):
        pass

    @abstractmethod
    def invalid_actions(self):
        pass

    @abstractmethod
    def valid_indexes(self):
        pass

    @abstractmethod
    def invalid_indexes(self):
        pass

    @abstractmethod
    def apply(self, action):
        pass

    @abstractmethod
    def result(self):
        pass

    def copy(self):
        return deepcopy(self)

    def next_copy(self, action):
        next_game = self.copy()
        next_game.apply(action)
        return next_game

    @abstractmethod
    def __str__(self):
        pass

    def __hash__(self):
        return hash(self.board.tobytes())

    def __eq__(self, other):
        return np.array_equal(self.board, other.board)

    @abstractproperty
    def current_player(self):
        pass

    @abstractproperty
    def last_action(self):
        pass

    @abstractproperty
    def board(self):
        pass