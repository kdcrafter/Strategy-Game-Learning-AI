from games import Tictactoe
from agents import Human, RandomAction, Minmax, TabularQlearning, MonteCarloTreeSearch, NeuralNetwork
from simulator import Simulator

from time import time
import numpy as np

if __name__ == '__main__':
    player = NeuralNetwork()

    # player learns to play tictactoe
    simulator = Simulator(Tictactoe(), player, RandomAction())
    simulator.play(num_games=10000)

    # player is tested
    simulator = Simulator(Tictactoe(), player, RandomAction())
    simulator.play(num_games=1000)

    simulator.set_opponent(Minmax())
    simulator.play(num_games=1000)