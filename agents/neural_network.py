from agent import Agent

import tensorflow as tf
from collections import deque

class NeuralNetwork(Agent):
    def __init__(self, discount_factor=1.0):
        super().__init__()

        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(9, activation=tf.nn.relu, input_shape=(9,)),
            tf.keras.layers.Dense(36, activation=tf.nn.relu),
            tf.keras.layers.Dense(36, activation=tf.nn.sigmoid),
            tf.keras.layers.Dense(9)
        ])

        loss_object = tf.keras.losses.MSE()
        self.optimizer = tf.keras.optimizersSGD(learning_rate=0.1)

        self.discount_factor = discount_factor

        self.game_history = deque()
        self.action_history = deque()

    def act(self, game):
        inputs = self.get_inputs(game)
        action = tf.argmax(self.model(inputs))
        self.update_history(game, action)
        return action

    def loss(self, x, y):
        y_ = self.model(x)
        return self.loss_obejct(y_true=y, y_pred=y_)

    def grad(self, inputs, targets):
        with tf.GradientTape() as tape:
            loss_value = loss(inputs, targets)
        return loss_value, tape.gradient(loss_value, self.model.trainable_variables)

    def get_inputs(self, game):
        return tf.convert_to_tensor(game.board)

    def get_targets(self, game, action, result, target_value):
        targets = np.zeros((9,))
        targets[game.get_invalid_actions()] = -1
        targets[action] = target_value
        return tf.convert_to_tensor(targets)

    def update_history(self, game, action):
        self.game_history.appendleft(game)
        self.action_history.appendleft(action)

    def gameover_callback(self, result):
        # if game ended before agent did anything
        if not self.game_history or not self.action_history:
            return

        next_game = self.game_history[0]
        next_action = self.action_history[0]

        inputs = self.get_inputs(next_game)
        target_value = -1 if next_game.current_player == -result else 1
        targets = self.get_targets(next_game, next_action, result, target_value)

        loss_value, grads = self.grad(inputs, targets)
        self.optimizer.apply_gradients(zip(grads, self.model.trainable_variables))

        for curr_game, curr_action in zip(list(self.game_history)[1:], list(self.action_history)[1:]):
            inputs = self.get_inputs(next_game)
            max_outputs_value = tf.reduce_max(self.model(inputs))
            targets = self.get_targets(curr_game, curr_action, result, self.discount_factor*max_outputs_value)

            loss_value, grads = self.grad(inputs, targets)
            self.optimizer.apply_gradients(zip(grads, self.model.trainable_variables))

            next_game = curr_game

        self.game_history.clear()
        self.action_history.clear()
