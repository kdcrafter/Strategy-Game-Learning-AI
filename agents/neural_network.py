'''
from learning_agent import LearningAgent
from config import TRAINING_AGENTS_DIRECTORY

import numpy as np
import tensorflow as tf
from collections import deque
import dill, os

# batch size parameter ?

"""
Sample Model (Tictactoe):

model = tf.keras.Sequential([
    tf.keras.layers.Reshape((9,), input_shape=(3,3,)),
    tf.keras.layers.Dense(9, activation=tf.nn.relu),
    tf.keras.layers.Dense(36, activation=tf.nn.relu),
    tf.keras.layers.Dense(36, activation=tf.nn.sigmoid),
    tf.keras.layers.Dense(9),
])
"""

class NeuralNetwork(LearningAgent):
    def __init__(self, model, learning_rate=0.1, discount_factor=1.0):
        super().__init__()

        self.policy_model = tf.keras.models.clone_model(model)
        self.target_model = tf.keras.models.clone_model(model)

        self.optimizer = tf.keras.optimizers.SGD(learning_rate=learning_rate)
        self.discount_factor = discount_factor

        self.game_history = deque()
        self.action_index_history = deque()

    def save(self, name):
        if not os.path.isdir(TRAINING_AGENTS_DIRECTORY):
            os.mkdir(TRAINING_AGENTS_DIRECTORY)

        filename = name + '.pickle'
        pathname = os.path.join(TRAINING_AGENTS_DIRECTORY, filename)

        with open(pathname, 'wb') as file:
            attributes = self.__dict__.copy()
            attributes['policy_model'] = self.get_weights(self.policy_model)
            attributes['target_model'] = self.get_weights(self.target_model)

            data = (self.__class__, attributes)
            dill.dump(data, file)

    def load(self, name):
        assert(os.path.isdir(TRAINING_AGENTS_DIRECTORY))

        filename = name + '.pickle'
        pathname = os.path.join(TRAINING_AGENTS_DIRECTORY, filename)

        with open(pathname, 'rb') as file:
            cls, attributes = dill.load(file)
            assert(self.__class__ == cls)

            self.assign_weights(attributes['policy_model'], self.policy_model)
            self.assign_weights(attributes['target_model'], self.target_model)
            del attributes['policy_model']
            del attributes['target_model']

            self.__dict__.update(attributes)

    def act(self, game):
        inputs = self.get_inputs(game)
        outputs = self.target_model(inputs)
        best_index = tf.argmax(outputs, axis=1)[0]
        best_action = game.actions()[best_index]

        if self.learning:
            self.update_history(game, best_index)

        return best_action

    def learn(self):
        self.learning = True
        self.gameover_callback = self.update_model

    def stop_learning(self):
        self.learning = False
        self.gameover_callback = None

    def loss(self, x, y):
        y_ = self.policy_model(x)
        return tf.keras.losses.MSE(y_true=y, y_pred=y_)

    def grad(self, inputs, targets):
        with tf.GradientTape() as tape:
            loss_value = self.loss(inputs, targets)
        return loss_value, tape.gradient(loss_value, self.policy_model.trainable_variables)

    def get_inputs(self, game):
        # get tensor of shape (1, board width, board height)
        inputs = tf.convert_to_tensor(game.board)
        return tf.reshape(inputs, (1,) + game.board.shape)

    def get_targets(self, game, action_index, target_value):
        num_actions = len(game.actions())

        targets = np.zeros(num_actions)
        targets[game.invalid_indexes()] = 0
        targets[action_index] = target_value

        # get tensor of shape (1, # of actions) where values of 0 are bad actions
        targets = tf.convert_to_tensor(targets)
        return tf.reshape(targets, (1, num_actions))

    def get_weights(self, model):
        return [layer.get_weights() for layer in model.layers]

    def assign_weights(self, weights_set, target_model):
        for weights, target_layer in zip(weights_set, target_model.layers):
            target_layer.set_weights(weights)

    def update_history(self, game, action):
        # games and actions are in reverse chronological order
        self.game_history.appendleft(game)
        self.action_index_history.appendleft(action)

    def update_model(self, game, result):
        # if game ended before agent did anything
        if not self.game_history or not self.action_index_history:
            return

        # get last game state and action index
        next_game = self.game_history.popleft()
        next_action_index = self.action_index_history.popleft()

        inputs = self.get_inputs(next_game)
        target_value = 0 if result == -next_game.current_player else 1 # 0 if loss else 1
        targets = self.get_targets(next_game, next_action_index, target_value)

        loss_value, grads = self.grad(inputs, targets)
        self.optimizer.apply_gradients(zip(grads, self.policy_model.trainable_variables))

        for curr_game, curr_action_index in zip(self.game_history, self.action_index_history):
            inputs = self.get_inputs(next_game)
            outputs = self.target_model(inputs)
            max_output = tf.reduce_max(outputs)
            targets = self.get_targets(curr_game, curr_action_index, self.discount_factor*max_output)

            loss_value, grads = self.grad(inputs, targets)
            self.optimizer.apply_gradients(zip(grads, self.policy_model.trainable_variables))

            next_game = curr_game

        policy_weights = self.get_weights(self.policy_model)
        self.assign_weights(policy_weights, self.target_model)

        self.game_history.clear()
        self.action_index_history.clear()

    def __str__(self):
        return 'NeuralNetwork'
'''