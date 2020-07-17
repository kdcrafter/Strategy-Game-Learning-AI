from agent import Agent

import numpy as np
from collections import defaultdict

class Minmax(Agent):
    def __init__(self):
        super().__init__()

        self.cache = defaultdict(lambda: None)

    def act(self, game):
        valid_actions, game_values = self.get_action_values(game)
        best_index = self.get_best_index(game.current_player, game_values)
        return valid_actions[best_index]

    def get_action_values(self, game):
        valid_actions = game.get_valid_actions()
        games = [game.get_next_copy(action) for action in valid_actions]
        game_values = np.array([self.get_game_value(game) for game in games])

        return valid_actions, game_values

    def get_game_value(self, game):
        winner = self.cache[game]
        if winner != None:
            return winner

        value = self.calc_game_value(game)
        self.cache[game] = value
        return value

    def calc_game_value(self, game):
        finished, winner = game.get_result()
        if finished:
            return winner

        valid_actions, game_values = self.get_action_values(game)
        return self.get_best_game_value(game.current_player, game_values)

    def get_best_game_value(self, current_player, game_values):
        if current_player == 1:
            return np.max(game_values)
        else:
            return np.min(game_values)

    def get_best_index(self, current_player, game_values):
        if current_player == 1:
            return np.argmax(game_values)
        else:
            return np.argmin(game_values)