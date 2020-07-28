from learning_agent import LearningAgent

from collections import defaultdict

class Minmax(LearningAgent):
    def __init__(self):
        super().__init__()
        self.cache = defaultdict(lambda: None)

    def act(self, game):
        valid_actions, game_values = self.get_action_values(game)
        best_index = self.get_best_index(game.current_player, game_values)
        return valid_actions[best_index]

    def learn(self):
        self.learning = True

    def stop_learning(self):
        self.learning = False

    def get_action_values(self, game):
        valid_actions = game.valid_actions()
        games = [game.next_copy(action) for action in valid_actions]
        game_values = [self.get_game_value(game) for game in games]

        return valid_actions, game_values

    def get_game_value(self, game):
        value = self.cache[game]
        if value != None:
            return value

        value = self.calc_game_value(game)

        if self.learning:
            self.cache[game] = value

        return value

    def calc_game_value(self, game):
        finished, winner = game.result()
        if finished:
            return winner

        valid_actions, game_values = self.get_action_values(game)
        return self.get_best_game_value(game.current_player, game_values)

    def get_best_game_value(self, current_player, game_values):
        if current_player == 1:
            return max(game_values)
        else:
            return min(game_values)

    def get_best_index(self, current_player, game_values):
        if current_player == 1:
            return game_values.index(max(game_values))
        else:
            return game_values.index(min(game_values))

    def __str__(self):
        return 'Minmax'