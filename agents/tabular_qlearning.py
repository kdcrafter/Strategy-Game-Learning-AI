from agent import Agent

import numpy as np
from collections import deque

class TabularQlearning(Agent):
    def __init__(self, epsilon=0.1, learning_rate=0.4, discount_factor=1.0, best_random_action=False):
        super().__init__()

        self.epsilon = epsilon
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor

        self.best_random_action = best_random_action

        self.qtable = {}

        self.game_history = deque()
        self.action_history = deque()

    def act(self, game):
        if np.random.uniform() < self.epsilon: # move randomly
            valid_actions = game.get_valid_actions()
            return np.random.choice(valid_actions, 1)[0]
        else: # move based on q values
            if self.best_random_action:
                return self.get_best_random_action(game)
            else:
                return self.get_best_action(game)

    def get_best_action(self, game):
        valid_actions, qvalues = self.get_action_qvalues(game)
        best_index = self.get_best_index(game.current_player, qvalues)
        return valid_actions[best_index]

    def get_best_random_action(self, game):
        valid_actions, qvalues = self.get_action_qvalues(game)

        best_qvalue = self.get_best_qvalue(game.current_player, qvalues)
        best_indexes = np.where(qvalues==best_qvalue)
        best_actions = valid_actions[best_indexes]

        return np.random.choice(best_actions, 1)[0]

    def get_action_qvalues(self, game):
        valid_actions = game.get_valid_actions()
        game_values = np.array([self.get_qvalue(game, action) for action in valid_actions])

        return valid_actions, game_values

    def get_qvalue(self, game, action):
        return self.qtable.get((game, action), 0.0)

    def set_qvalue(self, game, action, qvalue):
        self.qtable[(game, action)] = qvalue

    def update_qvalue(self, reward, game, action, next_game=None):
        if next_game is None:
            best_next_qvalue = 0.0
        else:
            if self.best_random_action:
                best_next_action = self.get_best_random_action(next_game)
            else:
                best_next_action = self.get_best_action(next_game)

            best_next_qvalue = self.get_qvalue(next_game, best_next_action)

        qvalue = self.get_qvalue(game, action)
        prior_value = (1 - self.learning_rate) * qvalue
        new_value = self.learning_rate * (reward + self.discount_factor*best_next_qvalue)
        self.set_qvalue(game, action, prior_value + new_value)

    def get_best_qvalue(self, current_player, qvalues):
        if current_player == 1:
            return np.max(qvalues)
        else:
            return np.min(qvalues)

    def get_best_index(self, current_player, qvalues):
        if current_player == 1:
            return np.argmax(qvalues)
        else:
            return np.argmin(qvalues)

    def end_turn_callback(self, game, action):
        self.game_history.appendleft(game)
        self.action_history.appendleft(action)

    def gameover_callback(self, result):
        next_game = self.game_history[0]
        next_action = self.action_history[0]

        self.update_qvalue(result, next_game, next_action)

        for curr_game, curr_action in zip(list(self.game_history)[1:], list(self.action_history)[1:]):
            self.update_qvalue(result, curr_game, curr_action, next_game)
            next_game = curr_game
        