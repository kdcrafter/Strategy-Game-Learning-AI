from collections import defaultdict

class Simulator():
    def __init__(self, game, player, opponent):
        self.game = game
        self.player = player
        self.opponent = opponent

        self.player_color = 1 # opponent color is -1
        self.first_score_set = defaultdict(lambda: Scores()) # scores when player goes first
        self.second_score_set = defaultdict(lambda: Scores()) # socres when player goes second

    def set_player(self, player):
        self.player = player

    def set_opponent(self, opponent):
        self.opponent = opponent

    def play(self, num_games=1):
        for i in range(num_games):
            self.game.setup()
    
            finished = False
            while not finished:
                if self.game.current_player == self.player_color:
                    action = self.player.act(self.game)
                else:
                    action = self.opponent.act(self.game)

                if self.player.end_turn_callbak != None:
                    self.player.end_turn_callback(self.game, action)
                if self.opponent.end_turn_callbak != None:
                    self.opponent.end_turn_callback(self.game, action)

                valid = self.game.apply(action)
                
                if not valid: # give other player the win
                    winner = -self.game.current_player
                    break
                    
                finished, winner = self.game.result()

            if self.player.gameover_callback != None:
                self.player.gameover_callback(self.game, winner)
            if self.opponent.gameover_callback != None:
                self.opponent.gameover_callback(self.game, winner)

            self.update_results(winner)
            self.player_color = -self.player_color

    def update_results(self, winner):
        players = (self.player, self.opponent)

        first_scores = self.first_score_set[players] # to ensure dicts have same keys
        second_scores = self.second_score_set[players]

        if self.player_color == 1: # color 1 always goes first
            scores = first_scores
        else:
            scores = second_scores

        if winner == self.player_color:
            scores.wins += 1
        elif winner == -self.player_color:
            scores.losses += 1
        else:
            scores.draws += 1

    def __str__(self):
        line = '|' + '-'*50 + '|\n'

        string = line
        string += f"|{'players':^20}"
        string += f"|{'first scores':^20}|{'second scores':^20}|\n"

        string += line
        string += f"|{'player':^10}|{'opponent':^10}"
        string += f"|{'wins':^20}|{'draws':^20}|{'losses':^20}"
        string += f"|{'wins':^20}|{'draws':^20}|{'losses':^20}|\n"
        string += line

        player_set = sorted(self.first_score_set.keys())

        for players in player_set:
            player, opponent = players

            string += f"|{player:^10}|{opponent:^10}"
            string += f"|{player.wins:^20}|{player.draws:^20}|{player.losses:^20}"
            string += f"|{opponent.wins:^20}|{opponent.draws:^20}|{opponent.losses:^20}|\n"
            string += line

        return string

def Scores():
    def __init__(self):
        self.wins = 0
        self.draws = 0
        self.losses = 0

    def __str__(self):
        return f'{self.wins} {self.draws} {self.losses}'
