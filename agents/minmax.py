from learning_agent import LearningAgent

from collections import defaultdict

class Minmax(LearningAgent):
    def __init__(self, max_depth=4):
        super().__init__()
        self.cache = defaultdict(lambda: (0, False)) # (game value, is game value final/certain)
        self.max_depth = max_depth # >= 1

    def act(self, game):
        valid_actions, game_values = self.get_action_values(game)
        best_index = self.get_best_index(game.current_player, game_values)
        return valid_actions[best_index]

    def learn(self):
        self.learning = True

    def stop_learning(self):
        self.learning = False

    def get_action_values(self, game, depth=0):
        valid_actions = game.valid_actions()
        games = [game.next_copy(action) for action in valid_actions]
        game_values = [self.get_game_value(game, depth+1) for game in games]

        return valid_actions, game_values

    def get_game_value(self, game, depth=0):
        value, is_final = self.cache[game]
        if is_final:
            return value

        value, is_final = self.calc_game_value(game, depth)

        if self.learning:
            self.cache[game] = (value, is_final)

        return value

    def calc_game_value(self, game, depth=0):
        finished, winner = game.result()
        if finished:
            return winner, True

        if depth == self.max_depth:
            return game.heuristic(), False

        valid_actions, game_values = self.get_action_values(game, depth)
        return self.get_best_game_value(game.current_player, game_values), True

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