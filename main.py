from games import Tictactoe
from agents import Human, RandomAction
from simulator import Simulator

if __name__ == '__main__':
    simulator = Simulator(Tictactoe(), Human(), RandomAction())
    simulator.play()
    print(simulator.num_player1_wins, simulator.num_player2_wins, simulator.num_draws)