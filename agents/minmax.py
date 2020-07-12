from agent import Agent

import numpy as np
from collections import defaultdict

class Minmax(Agent):
    def __init__(self):
        super().__init__()

        self.cache = defaultdict(lambda: None)

    def act(self, game):
        valid_actions = game.get_valid_actions()
        game_values = np.array([self.get_next_value(game, action) for action in valid_actions])

        # TODO: see if their should be a option to choose best options randomly

        if game.current_player == 1:
            best_value = np.max(game_values)
        else:
            best_value = np.min(game_values)

        best_indexes = np.where(game_values==best_value)
        best_actions = valid_actions[best_indexes]

        return np.random.choice(best_actions, 1)[0]

    def get_next_value(self, game, action):
        next_game = game.get_copy()
        next_game.apply(action)
        return self.get_value(next_game)

    def get_value(self, game):
        winner = self.cache[game]
        if winner != None:
            return winner

        finished, winner = game.get_result()
        if finished:
            self.cache[game] = winner
            return winner

        valid_actions = game.get_valid_actions()
        game_values = np.array([self.get_next_value(game, action) for action in valid_actions])

        if game.current_player == 1:
            return np.max(game_values)
        else:
            return np.min(game_values)