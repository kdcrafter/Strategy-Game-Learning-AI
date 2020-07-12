from games import Tictactoe
from agents import Human, RandomAction, Minmax
from simulator import Simulator

from time import time
import numpy as np

if __name__ == '__main__':
    player1 = RandomAction()
    player2 = Minmax()
    simulator = Simulator(Tictactoe(), player1, player2)

    start = time()
    simulator.play(num_games=1)
    print(time() - start)
    print(len(player2.cache))

    simulator.play(num_games=1000)
    print(len(player2.cache))

    start = time()
    simulator.play(num_games=1)
    print(time() - start)
    print(len(player2.cache))

    print(simulator.num_player1_wins, simulator.num_player2_wins, simulator.num_draws)