from agent import Agent

import random

class RandomAction(Agent):
    def __init__(self):
        super().__init__()

    def act(self, game):
        valid_actions = game.valid_actions()
        return random.choice(valid_actions)

    def __str__(self):
        return 'RandomAction'
