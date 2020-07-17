from agent import Agent

import numpy as np
import math

class MonteCarloTreeSearch(Agent):
    def __init__(self, exploration_constant=math.sqrt(2)):
        super().__init__()

        self.cache = {}
        self.game_history = []

        self.exploration_constant = exploration_constant

    def act(self, game):
        valid_actions = game.get_valid_actions()
        games = [game.get_next_copy(action) for action in valid_actions]

        parent = self.get_child(game)
        children = np.array([self.get_child(game) for game in games])
        ucb1_values = np.array([self.get_ucb1(parent, child) for child in children])

        best_index = np.argmax(ucb1_values)
        best_action = valid_actions(best_index)


        return np.argmax()

    def get_child(self, game):
        return self.cache.get(game, Node())

    def get_ucb1(self, parent, child):
        if child.num_visits == 0:
            return float('inf')

        success_rate = child.num_win_draws / child.num_visits
        exploration_term = self.exploration_constant * math.sqrt(math.log(parent.num_visits) / child.num_visits)
        return success_rate + exploration_term

    def update_history(self):
        self.game_history.append()

    def game_overcallback(self, result):
        for game in self.game_history:
            node = self.get_node(game)

            node.num_visits += 1

            if result == game.current_player or result == 0:
                node.num_win_draws += 1

        self.game_history.clear()

class Node():
    def __init__(self):
        self.num_win_draws = 0
        self.num_visits = 0

