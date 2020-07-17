from games import Tictactoe
from agents import Human, RandomAction, Minmax, TabularQlearning
from simulator import Simulator

from time import time
import numpy as np

if __name__ == '__main__':
    playera = RandomAction()
    playerb = TabularQlearning(epsilon=0.1, learning_rate=0.9, discount_factor=1.0, init_qvalue=0.0)

    simulator = Simulator(Tictactoe(), playerb, playera)
    simulator.play(num_games=500)
    print(simulator.num_player1_wins, simulator.num_player2_wins, simulator.num_draws)

    simulator = Simulator(Tictactoe(), playera, playerb)
    simulator.play(num_games=500)
    print(simulator.num_player1_wins, simulator.num_player2_wins, simulator.num_draws)