from abc import ABC, abstractmethod, abstractproperty

class Agent(ABC):
    def __init__(self):
        super().__init__()

        self.end_turn_callback = None
        self.gameover_callback = None

    @abstractmethod
    def act(self, game):
        pass

    @abstractmethod
    def __str__(self):
        pass