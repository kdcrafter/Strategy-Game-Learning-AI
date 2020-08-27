from games import Tictactoe, Connect4
from agents import Human, RandomAction, FirstAction, Minmax, TabularQlearning, MonteCarloTreeSearch
from simulator import Simulator

from codetiming import Timer

if __name__ == '__main__':
    # set up
    game = Tictactoe()
    player = Minmax(8)

    random_action = RandomAction()
    minmax = Minmax(8)
    # minmax.load('connect4_minmax1')

    # player learns to play game
    simulator = Simulator(game, player, [random_action, minmax])
    simulator.play(num_games=800)

    print(simulator)

    # player is stored
    player.stop_learning()
    player.save('tictactoe_minmax8')

    # player is tested
    simulator.reset_scores()
    simulator.play(num_games=200)

    print(simulator)