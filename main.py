from games import Tictactoe
from agents import Human, RandomAction, Minmax, TabularQlearning, MonteCarloTreeSearch, NeuralNetwork
from simulator import Simulator

import numpy as np
import tensorflow as tf

if __name__ == '__main__':
    # set up
    game = Tictactoe()

    model = tf.keras.Sequential([
        tf.keras.layers.Reshape((9,), input_shape=(3,3,)),
        tf.keras.layers.Dense(9, activation=tf.nn.relu),
        tf.keras.layers.Dense(36, activation=tf.nn.relu),
        tf.keras.layers.Dense(36, activation=tf.nn.sigmoid),
        tf.keras.layers.Dense(9),
    ])
    player = NeuralNetwork(model)

    random_action = RandomAction()
    minmax = Minmax()
    minmax.load('tictactoe_minmax')

    # player learns to play game
    simulator = Simulator(game, player, [random_action, minmax])
    simulator.play(num_games=100000)

    # player is stored
    player.stop_learning()
    player.save('tictactoe_neural_network')

    print(simulator)

    # player is tested
    simulator.reset_scores()
    simulator.play(num_games=400)

    print(simulator)