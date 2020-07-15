from games import Tictactoe
from agents import Human, RandomAction, Minmax, TabularQlearning
from simulator import Simulator

from time import time
import numpy as np

if __name__ == '__main__':
    player1 = RandomAction()
    player2 = TabularQlearning()
    simulator = Simulator(Tictactoe(), player1, player2)

    simulator.play(num_games=1000)
    print(simulator.num_player1_wins, simulator.num_player2_wins, simulator.num_draws)

    simulator.reset_results()
    player2.epsilon = 0.0
    simulator.play(num_games=10)
    print(simulator.num_player1_wins, simulator.num_player2_wins, simulator.num_draws)