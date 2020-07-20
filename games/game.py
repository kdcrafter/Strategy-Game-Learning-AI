from abc import ABC, abstractmethod, abstractproperty
import numpy as np

class Game(ABC):
    @abstractmethod
    def __init__(self, current_player=1, board=None):
        super().__init__()

    @abstractmethod
    def setup(self, current_player=1, board=None):
        pass

    @abstractmethod
    def get_actions(self):
        pass

    @abstractmethod
    def get_valid_actions(self):
        pass

    @abstractmethod
    def get_invalid_actions(self):
        pass

    @abstractmethod
    def get_copy(self):
        pass

    @abstractmethod
    def get_next_copy(self, action):
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

    def __hash__(self):
        state = bytearray(self.board.tobytes())
        state.append(self.current_player+1) # append either 2 or 0 (can't be -1)
        return hash(bytes(state))

    def __eq__(self, other):
        return np.array_equal(self.board, other.board) and self.current_player == other.current_player

    @abstractproperty
    def current_player(self):
        pass

    @abstractproperty
    def board(self):
        pass