from games import Tictactoe, Connect4
from agents import Human, RandomAction, Minmax, TabularQlearning, MonteCarloTreeSearch
from simulator import Simulator

if __name__ == '__main__':
    # set up
    game = Connect4()
    player = Minmax(1)

    random_action = RandomAction()
    # minmax = Minmax()
    # minmax.load('connect4_minmax1')

    # player learns to play game
    simulator = Simulator(game, player, [random_action])
    simulator.play(num_games=8)

    print(simulator)

    # player is stored
    player.stop_learning()
    player.save('connect4_minmax_test')

    # player is tested
    simulator.reset_scores()
    simulator.play(num_games=2)

    print(simulator)