from agent import Agent

class Human(Agent):
    def __init__(self):
        super().__init__()

        self.end_turn_callback = self.show_game
        self.gameover_callback = self.show_result

    def act(self, game):
        print(game)
        print('Actions:', game.valid_actions())
        print('Input:', end=' ')
        action = eval(input())
        print()

        return action

    def show_game(self, game, action):
        print(game)
        print()

    def show_result(self, game, result):
        print(game)
        print('Winner:', result)
        print()

    def __str__(self):
        return 'Human'