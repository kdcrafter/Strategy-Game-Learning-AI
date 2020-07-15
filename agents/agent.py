from abc import ABC, abstractmethod, abstractproperty

class Agent(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def act(self, game):
        pass

    def gameover_callback(self, result):
        pass