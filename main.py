from games import Tictactoe
from agents import Human, RandomAction, Minmax
from simulator import Simulator

if __name__ == '__main__':
    simulator = Simulator(Tictactoe(), RandomAction(), Minmax())
    simulator.play(num_games=1)
    print(simulator.num_player1_wins, simulator.num_player2_wins, simulator.num_draws)