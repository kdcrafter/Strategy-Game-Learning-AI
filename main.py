from games import Tictactoe
from agents import Human, RandomAction, Minmax, TabularQlearning, MonteCarloTreeSearch, NeuralNetwork
from simulator import Simulator

from time import time
import numpy as np

if __name__ == '__main__':
    playera = NeuralNetwork()
    playerb = RandomAction()

    simulator = Simulator(Tictactoe(), playera, playerb)
    simulator.play(num_games=10000)
    print(simulator.num_player1_wins, simulator.num_player2_wins, simulator.num_draws)

    simulator = Simulator(Tictactoe(), playerb, playera)
    simulator.play(num_games=10000)
    print(simulator.num_player1_wins, simulator.num_player2_wins, simulator.num_draws)

    simulator = Simulator(Tictactoe(), playera, playerb)
    simulator.play(num_games=100)
    print(simulator.num_player1_wins, simulator.num_player2_wins, simulator.num_draws)

    simulator = Simulator(Tictactoe(), playerb, playera)
    simulator.play(num_games=100)
    print(simulator.num_player1_wins, simulator.num_player2_wins, simulator.num_draws)