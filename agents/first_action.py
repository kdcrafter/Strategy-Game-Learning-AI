from agent import Agent

class FirstAction(Agent):
    def __init__(self):
        super().__init__()

    def act(self, game):
        valid_actions = game.valid_actions()
        return valid_actions[0]

    def __str__(self):
        return 'FirstAction'