

class Simulator():
    def __init__(self, game, player1, player2):
        self.game = game
        self.player1 = player1 # agent acting as player1 (1)
        self.player2 = player2 # agent acting as player2 (-1)

        self.num_player1_wins = 0
        self.num_player2_wins = 0
        self.num_draws = 0

    def reset_results(self):
        self.num_player1_wins = 0
        self.num_player2_wins = 0
        self.num_draws = 0
    
    def play(self, num_games=1):
        for i in range(num_games):
            self.game.setup()
    
            finished = False
            while not finished:
                if self.game.current_player == 1:
                    action = self.player1.act(self.game) # TODO: make sure a copy of the game is passed
                else:
                    action = self.player2.act(self.game)

                finished, winner = self.game.apply(action)

            self.update_results(winner)

    def update_results(self, winner):
        if winner == 1:
            self.num_player1_wins += 1
        elif winner == -1:
            self.num_player2_wins += 1
        else:
            self.draws += 1