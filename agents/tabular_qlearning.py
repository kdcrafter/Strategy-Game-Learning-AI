from agent import Agent

import numpy as np
from collections import defaultdict

class TabularQlearning(Agent):
    def __init__(self, epsilon=0.1):
        super().__init__()

        self.epsilon = epsilon

        self.qtable1 = defaultdict(lambda: 0.0)
        self.qtable2 = defaultdict(lambda: 0.0)

    def act(self, game):
        if np.random.uniform() < self.epsilon: # move randomly
            valid_actions = game.get_valid_actions()
            return np.random.choice(valid_actions, 1)[0]
        else: # move based on q values
            valid_actions = game.get_valid_actions()
            qvalues = np.array([get_average_qvalue(game, action) for action in valid_actions])
            best_index = np.argmax(qvalues)

            return valid_actions[best_index]

    def get_average_qvalue(self, game, action):
        next_game = game.get_copy()
        next_game.apply(action)
        return (self.qtable[next_game] + self.qtable[next_game]) / 2

        