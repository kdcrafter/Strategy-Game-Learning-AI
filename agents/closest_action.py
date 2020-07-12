from agent import Agent

class ClosestAction(Agent):
    def __init__(self, action):
        super().__init__()

        self.action = action

    def act(self, game):
        valid_actions = game.get_valid_actions()
        return min(valid_actions, key=lambda x: abs(self.action-x))
