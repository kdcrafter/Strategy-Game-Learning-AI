from abc import ABC, abstractmethod, abstractproperty

class Agent(ABC):
    def __init__(self):
        super().__init__()

        self.end_turn_callback = None
        self.gameover_callback = None

        # player color ?
        # minmax agent would only need to use max

    @abstractmethod
    def act(self, game):
        pass