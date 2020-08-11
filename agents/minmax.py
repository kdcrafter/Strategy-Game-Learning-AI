from learning_agent import LearningAgent

from collections import defaultdict

class Minmax(LearningAgent):
    def __init__(self, max_depth=4):
        super().__init__()
        self.cache = defaultdict(lambda: (0, False)) # (game value, is game value final/certain)
        self.max_depth = max_depth # >= 0

    def learn(self):
        self.learning = True

    def stop_learning(self):
        self.learning = False

    @profile
    def act(self, game):
        valid_actions = game.valid_actions()
        games = [game.next_copy(action) for action in valid_actions]

        disjointed_game_values = [self.get_game_values(game) for game in games]
        game_values, is_final_values = zip(*disjointed_game_values)

        best_index = self.get_best_index(game.current_player, game_values)
        game_value = game_values[best_index]
        is_final = is_final_values[best_index]

        if self.learning:
            self.cache[game] = (game_value, is_final)

        return valid_actions[best_index]

    @profile
    def get_game_values(self, game, depth=0):
        if not self.learning:
            return self.cache[game]

        value, is_final = self.cache[game]
        if is_final:
            self.cache[game] = (value, True)
            return self.cache[game]

        finished, winner = game.result()
        if finished:
            self.cache[game] = (winner, True)
            return self.cache[game]

        if depth == self.max_depth:
            self.cache[game] = (game.heuristic(), False)
            return self.cache[game]

        valid_actions = game.valid_actions()
        games = [game.next_copy(action) for action in valid_actions]

        disjointed_game_values = [self.get_game_values(game, depth+1) for game in games]
        game_values, is_final_values = zip(*disjointed_game_values)

        best_index = self.get_best_index(game.current_player, game_values)
        game_value = game_values[best_index]
        is_final = is_final_values[best_index]
        self.cache[game] = (game_value, is_final)

        return game_value, is_final

    @profile
    def get_best_index(self, current_player, game_values):
        if current_player == 1:
            return game_values.index(max(game_values))
        else:
            return game_values.index(min(game_values))

    def __str__(self):
        return 'Minmax'