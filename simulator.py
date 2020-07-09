class Simulator():
    def __init__(self, game, player1, player2):
        self.game = game
        self.player1 = player1 # agent acting as player1 (1)
        self.player2 = player2 # agent acting as player2 (-1)

        self.num_player1_wins = 0
        self.num_player2_wins = 0
        self.num_draws = 0
    
    def play(self, num_games=1):
        for i in range(num_games):
            self.game.setup() # reset game to initial state
    
            finished = False
            while not finished:
                if self.game.current_player == 1:
                    action = self.player1.act(self.game.get_copy())
                else:
                    action = self.player2.act(self.game.get_copy())

                valid = self.game.apply(action)
                
                if not valid: # give other player the win
                    winner = -self.game.current_player
                    break
                    
                finished, winner = self.game.get_result()

            self.update_results(winner)

    def update_results(self, winner):
        if winner == 1:
            self.num_player1_wins += 1
        elif winner == -1:
            self.num_player2_wins += 1
        else:
            self.num_draws += 1