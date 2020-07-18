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

        parent = self.get_node(game)
        children = np.array([self.get_node(game) for game in games])

        ucb1_values = np.array([child.get_ucb1(self.exploration_constant) for child in children])
        best_index = np.argmax(ucb1_values)
        return valid_actions[best_index]

    def get_node(self, game):
        if not game in self.cache:
            node = Node()
            self.cache[game] = node
            return node
        else:
            return self.cache[game]

    def end_turn_callback(self, game, action):
        self.game_history.append(game)

        next_game = game.get_next_copy(action)
        finished, winner = game.get_result()

        if finished:
            self.game_history.append(next_game)

    def gameover_callback(self, result):
        # if game ended before agent did anything
        if not self.game_history:
            return

        parent_game = self.game_history[0]

        parent_node = self.get_node(parent_game)
        parent_node.num_visits += 1
        if result == -parent_game.current_player or result == 0:
            parent_node.num_win_draws += 1

        for game in self.game_history[1:]:
            node = self.get_node(game)
            node.num_visits += 1
            if result == -game.current_player or result == 0:
                node.num_win_draws += 1

            node.parents.add(parent_node)
            parent_node = node

        self.game_history.clear()

class Node():
    def __init__(self):
        self.parents = set()

        self.num_win_draws = 0
        self.num_visits = 0

    def get_parent_visits(self):
        sum = 0
        for parent in self.parents:
            sum += parent.num_visits
        return sum

    def get_ucb1(self, exploration_constant):
        if self.num_visits == 0:
            return float('inf')

        success_rate = self.num_win_draws / self.num_visits
        exploration_term = exploration_constant * math.sqrt(math.log(self.get_parent_visits()) / self.num_visits)
        return success_rate + exploration_term

