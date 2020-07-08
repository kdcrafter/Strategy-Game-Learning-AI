from game import TictactoeGame
from agent import RandomAgent

if __name__ == '__main__':
    player1 = RandomAgent()
    player2 = RandomAgent()
    tictactoe = TictactoeGame(player1, player2)

    tictactoe.play(num_games=100)

    print(tictactoe.num_player1_wins, tictactoe.num_player2_wins, tictactoe.num_draws)