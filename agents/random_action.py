import numpy as np

from agent import Agent

class RandomAction(Agent):
    def __init__(self):
        super().__init__()

    def act(self, game):
        valid_actions = game.get_valid_actions()
        return np.random.choice(valid_actions, 1)[0]