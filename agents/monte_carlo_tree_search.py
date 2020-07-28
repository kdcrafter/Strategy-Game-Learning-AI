from learning_agent import LearningAgent

import math
from collections import defaultdict, deque
from functools import reduce 

class MonteCarloTreeSearch(LearningAgent):
    def __init__(self, exploration_constant=math.sqrt(2)):
        super().__init__()

        self.nodes = defaultdict(lambda: Node())
        self.game_history = deque()

        self.exploration_constant = exploration_constant

    def act(self, game):
        valid_actions = game.valid_actions()
        games = [game.next_copy(action) for action in valid_actions]
        children = [self.nodes[game] for game in games]

        if self.learning:
            values = [child.ucb1(self.exploration_constant) for child in children]
        else:
            values = [child.success_rate() for child in children]
    
        best_index = values.index(max(values))
        return valid_actions[best_index]

    def learn(self):
        self.learning = True
        self.end_turn_callback = self.update_history
        self.gameover_callback = self.update_nodes

    def stop_learning(self):
        self.learning = False
        self.end_turn_callback = None
        self.gameover_callback = None

    def update_history(self, game, action):
        self.game_history.append(game.copy())

    def update_nodes(self, game, result):
        parent_game = self.game_history[0]

        parent_node = self.nodes[parent_game]
        parent_node.visits += 1

        #if loss, count as win
        if result == -parent_game.current_player or result == 0:
            parent_node.win_draws += 1

        for game in list(self.game_history)[1:]:
            node = self.nodes[game]
            node.visits += 1
            if result == -game.current_player or result == 0:
                node.win_draws += 1

            node.parents.add(parent_node)
            parent_node = node

        self.game_history.clear()

    def __str__(self):
        return 'MCTS'

class Node():
    def __init__(self):
        self.parents = set()

        self.win_draws = 0
        self.visits = 0

    def success_rate(self):
        if self.visits == 0:
            return float('inf')

        return self.win_draws / self.visits

    def parent_visits(self):
        return reduce(lambda s,node: s+node.visits, self.parents, 0)

    def ucb1(self, exploration_constant):
        if self.visits == 0:
            return float('inf')

        success_rate = self.win_draws / self.visits
        exploration_term = exploration_constant * math.sqrt(math.log(self.parent_visits()) / self.visits)
        return success_rate + exploration_term
