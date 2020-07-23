from agent import Agent

class Human(Agent):
    def __init__(self):
        super().__init__()

    def act(self, game):
        print(game)
        print('Actions:', game.valid_actions())
        print('Input:', end=' ')
        return eval(input())