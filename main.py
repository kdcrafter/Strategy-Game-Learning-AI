from games import Tictactoe
from agents import Human, RandomAction, Minmax, TabularQlearning, MonteCarloTreeSearch
from simulator import Simulator

from time import time
import numpy as np

if __name__ == '__main__':
    # set up
    game = Tictactoe()

    player = MonteCarloTreeSearch()
    random_action = RandomAction()

    minmax = Minmax()
    minmax.load('tictactoe_minmax')

    # player learns to play tictactoe
    simulator = Simulator(game, player, [random_action, minmax])
    simulator.play(num_games=100000)

    # player is stored
    player.stop_learning()
    player.save('tictactoe_mcts')

    print(simulator)

    # player is tested
    simulator.reset_scores()
    simulator.play(num_games=400)

    print(simulator)