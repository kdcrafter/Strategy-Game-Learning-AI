from games import Tictactoe
from agents import Human, RandomAction, Minmax, TabularQlearning
from simulator import Simulator

from time import time
import numpy as np

if __name__ == '__main__':
    player1 = RandomAction()
    player2 = TabularQlearning(epsilon=0.5, learning_rate=0.99, discount_factor=1.0, init_qvalue=0.0)
    simulator = Simulator(Tictactoe(), player1, player2)

    simulator.play(num_games=1000)
    print(simulator.num_player1_wins, simulator.num_player2_wins, simulator.num_draws)

    simulator.reset_results()
    player2.epsilon = 0.0
    simulator.play(num_games=100)
    print(simulator.num_player1_wins, simulator.num_player2_wins, simulator.num_draws)