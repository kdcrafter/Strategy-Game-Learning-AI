from agent import Agent

import numpy as np
from collections import defaultdict, deque

class TabularQlearning(Agent):
    def __init__(self, epsilon=0.1, learning_rate=0.4, discount_factor=1.0):
        super().__init__()

        self.epsilon = epsilon
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor

        self.qtable = {}

        self.game_history = deque()
        self.action_history = deque()

    def act(self, game):
        if np.random.uniform() < self.epsilon: # move randomly
            valid_actions = game.get_valid_actions()
            return np.random.choice(valid_actions, 1)[0]
        else: # move based on q values
            valid_actions = game.get_valid_actions()
            qvalues = np.array([self.qtable.get(game.get_next_copy(action), 0.0) for action in valid_actions])
            
            if game.current_player == 1:
                best_value = np.max(qvalues)
            else:
                best_value = np.min(qvalues)

            best_indexes = np.where(qvalues==best_value)
            best_actions = valid_actions[best_indexes]

            return np.random.choice(best_actions, 1)[0]

    def end_turn_callback(self, game, action):
        self.game_history.appendleft(game)
        self.action_history.appendleft(action)

    def gameover_callback(self, result):
        next_game = self.game_history[0]
        next_action = self.action_history[0]

        qvalue = self.qtable.get((next_game, next_action), 0.0)
        prior_value = (1 - self.learning_rate) * qvalue
        new_value = self.learning_rate * (result + self.discount_factor*0.0)
        self.qtable[(next_game, next_action)] = prior_value + new_value

        for curr_game, curr_action in zip(list(self.game_history)[1:], list(self.action_history)[1:]):
            valid_actions = next_game.get_valid_actions()
            qvalues = np.array([self.qtable.get(next_game.get_next_copy(action), 0.0) for action in valid_actions])

            if next_game.current_player == 1:
                best_value = np.max(qvalues)
            else:
                best_value = np.min(qvalues)

            best_next_indexes = np.where(qvalues==best_value)
            best_next_actions = valid_actions[best_next_indexes]
            best_next_action = np.random.choice(best_next_actions, 1)[0]
            best_next_qvalue = self.qtable.get((next_game, best_next_action), 0.0)

            qvalue = self.qtable.get((curr_game, curr_action), 0.0)
            prior_value = (1 - self.learning_rate) * qvalue
            new_value = self.learning_rate * (result + self.discount_factor*best_next_qvalue)
            self.qtable[(next_game, next_action)] = prior_value + new_value

            next_game = curr_game
        