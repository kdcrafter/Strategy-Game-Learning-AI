from agent import Agent

from collections import deque
import math

# TODO: implement a double qlearning version

class TabularQlearning(LearningAgent):
    def __init__(self, epsilon_init=0.5, epsilon_drop_rate=0.5, epsilon_drop_step=10, learning_rate_init=0.5, learning_rate_drop_rate=0.5, learning_rate_drop_step=10, discount_factor=1.0):
        super().__init__()

        self.epsilon = epsilon_init
        self.epsilon_init = epsilon_init
        self.epsilon_drop_rate = epsilon_drop_rate
        self.epsilon_drop_step = epsilon_drop_step

        self.learning_rate = learning_rate_init
        self.learning_rate_init = learning_rate_init
        self.learning_rate_drop_rate = learning_rate_drop_rate
        self.learning_rate_drop_step = learning_rate_drop_step 

        self.games_played = 0
        self.discount_factor = discount_factor
        self.init_qvalue = init_qvalue

        self.qtable = {}

        self.game_history = deque()
        self.action_history = deque()

    def act(self, game):
        if random.uniform() < self.epsilon: # move randomly
            valid_actions = game.valid_actions()
            action = random.choice(valid_actions)
        else: # move based on q values
            action = self.get_best_action(game)

        if self.learning:
            self.update_history(game, action)

        return action

    def learn(self):
        self.learning = True
        self.epsilon = self.epsilon_init
        self.learning_rate = self.learning_rate_init
        self.gameover_callback = self.update_qtable

    def stop_learning(self):
        self.learning = False
        self.epsilon = 0.0
        self.learning_rate = 0.00001
        self.gameover_callback = None

    def get_best_action(self, game):
        valid_actions, qvalues = self.get_action_qvalues(game)
        best_index = self.get_best_index(game.current_player, qvalues)
        return valid_actions[best_index]

    def get_action_qvalues(self, game):
        valid_actions = game.valid_actions()
        game_values = [self.get_qvalue(game, action) for action in valid_actions]

        return valid_actions, game_values

    def get_qvalue(self, game, action):
        return self.qtable.get((game, action), 0.0)

    def set_qvalue(self, game, action, qvalue):
        self.qtable[(game, action)] = qvalue

    def update_qvalue(self, reward, game, action, next_game=None):
        if next_game is None:
            best_next_qvalue = 0.0
        else:
            best_next_action = self.get_best_action(next_game)
            best_next_qvalue = self.get_qvalue(next_game, best_next_action)

        qvalue = self.get_qvalue(game, action)
        prior_value = (1 - self.learning_rate) * qvalue
        new_value = self.learning_rate * (reward + self.discount_factor*best_next_qvalue)
        self.set_qvalue(game, action, prior_value + new_value)

    def get_best_qvalue(self, current_player, qvalues):
        if current_player == 1:
            return max(qvalues)
        else:
            return min(qvalues)

    def get_best_index(self, current_player, qvalues):
        if current_player == 1:
            return qvalues.index(max(qvalues))
        else:
            return qvalues.index(min(qvalues))

    def get_decay(self, init, drop_rate, drop_step):
        exponent = math.floor((1+self.games_played) / drop_step)
        return init * math.pow(drop_rate, exponent)

    def update_history(self, game, action):
        self.game_history.appendleft(game)
        self.action_history.appendleft(action)

    def update_qtable(self, game, result):
        # if game ended before agent did anything
        if not self.game_history or not self.action_history:
            return

        next_game = self.game_history[0]
        next_action = self.action_history[0]

        self.update_qvalue(result, next_game, next_action)

        for curr_game, curr_action in zip(list(self.game_history)[1:], list(self.action_history)[1:]):
            self.update_qvalue(result, curr_game, curr_action, next_game)
            next_game = curr_game

        self.game_history.clear()
        self.action_history.clear()

        self.games_played += 1

        if self.games_played % self.epsilon_drop_step == 0:
            self.epsilon = self.get_decay(self.epsilon_init, self.epsilon_drop_rate, self.epsilon_drop_step)

        if self.games_played % self.learning_rate_drop_step == 0:     
            self.learning_rate = self.get_decay(self.learning_rate_init, self.learning_rate_drop_rate, self.learning_rate_drop_step)

