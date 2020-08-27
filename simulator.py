from collections import defaultdict
from itertools import cycle

from codetiming import Timer

class Simulator():
    def __init__(self, game, player, opponents):
        self.game = game
        self.player = player
        self.opponents = cycle(opponents)

        self.player_color = 1 # opponent color is -1

        # (player, opponent) -> (player is first scores, player if second scores)
        self.player_scores = defaultdict(lambda: (Scores(), Scores()))

    def reset_scores(self):
        self.player_scores = defaultdict(lambda: (Scores(), Scores()))

    def play(self, num_games=1):
        self.opponent = next(self.opponents)
        print_rate = num_games//100 if num_games >= 100 else 1

        for i in range(num_games):
            if i % print_rate == 0:
                print(f'Game: {i} / {num_games}', end='\r')

            self.game.setup()
    
            finished = False
            while not finished:
                if self.game.current_player == self.player_color:
                    action = self.player.act(self.game.copy())
                else:
                    action = self.opponent.act(self.game.copy())

                if self.player.end_turn_callback != None:
                    self.player.end_turn_callback(self.game.copy(), action)
                if self.opponent.end_turn_callback != None:
                    self.opponent.end_turn_callback(self.game.copy(), action)

                valid = self.game.apply(action)
                
                if not valid: # give other player the win
                    winner = -self.game.current_player
                    break
                    
                finished, winner = self.game.result()

            if self.player.gameover_callback != None:
                self.player.gameover_callback(self.game.copy(), winner)
            if self.opponent.gameover_callback != None:
                self.opponent.gameover_callback(self.game.copy(), winner)

            self.update_results(winner)
            self.player_color = -self.player_color

            # so player goes against opponent first then second then switches to the next opponent
            if self.player_color == 1:
                self.opponent = next(self.opponents)

        print() # newline

    def update_results(self, winner):
        players = (self.player, self.opponent)
        scores = self.player_scores[players][0 if self.player_color == 1 else 1]

        if winner == self.player_color:
            scores.wins += 1
        elif winner == -self.player_color:
            scores.losses += 1
        else:
            scores.draws += 1

    def __str__(self):
        line = '|' + '-'*107 + '|\n'

        string = line
        string += f"|{'players':^41}"
        string += f"|{'first scores':^32}|{'second scores':^32}|\n"

        string += line
        string += f"|{'player':^20}|{'opponent':^20}"
        string += f"|{'wins':^10}|{'draws':^10}|{'losses':^10}"
        string += f"|{'wins':^10}|{'draws':^10}|{'losses':^10}|\n"
        string += line

        for players, scores in self.player_scores.items():
            player, opponent = players
            first_scores, second_scores = scores

            string += f"|{player.__str__():^20}|{opponent.__str__():^20}"
            string += f"|{first_scores.wins:^10}|{first_scores.draws:^10}|{first_scores.losses:^10}"
            string += f"|{second_scores.wins:^10}|{second_scores.draws:^10}|{second_scores.losses:^10}|\n"
            string += line

        return string

class Scores():
    def __init__(self):
        self.wins = 0
        self.draws = 0
        self.losses = 0

    def __str__(self):
        return f'{self.wins} {self.draws} {self.losses}'
