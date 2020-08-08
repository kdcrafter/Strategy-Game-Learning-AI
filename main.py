from games import Tictactoe, Connect4
from agents import Human, RandomAction, Minmax, TabularQlearning, MonteCarloTreeSearch, NeuralNetwork
from simulator import Simulator

if __name__ == '__main__':
    # set up
    game = Connect4()
    player = Minmax()

    random_action = RandomAction()
    minmax = Minmax()
    # minmax.load('connect4_minmax')

    # player learns to play game
    simulator = Simulator(game, player, [random_action, minmax])
    simulator.play(num_games=100)

    # player is stored
    player.stop_learning()
    player.save('connect4_minmax')

    print(simulator)

    # player is tested
    simulator.reset_scores()
    simulator.play(num_games=400)

    print(simulator)