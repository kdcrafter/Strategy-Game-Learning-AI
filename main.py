from games import Tictactoe, Connect4
from agents import Human, RandomAction, Minmax, TabularQlearning, MonteCarloTreeSearch, NeuralNetwork
from simulator import Simulator

import tensorflow as tf

if __name__ == '__main__':
    # set up
    game = Connect4()

    model = tf.keras.Sequential([
        tf.keras.layers.Reshape((42,), input_shape=(6,7,)),
        tf.keras.layers.Dense(42, activation=tf.nn.relu),
        tf.keras.layers.Dense(56, activation=tf.nn.relu),
        tf.keras.layers.Dense(28, activation=tf.nn.sigmoid),
        tf.keras.layers.Dense(7),
    ])
    player = NeuralNetwork(model)

    random_action = RandomAction()
    minmax = Minmax()
    minmax.load('connect4_minmax1')

    # player learns to play game
    simulator = Simulator(game, player, [minmax, random_action])
    simulator.play(num_games=800)

    print(simulator)

    # player is stored
    player.stop_learning()
    player.save('connect4_neural_network')

    # player is tested
    simulator.reset_scores()
    simulator.play(num_games=200)

    print(simulator)