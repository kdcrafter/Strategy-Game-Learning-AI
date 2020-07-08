from game import Game
import numpy as np

ACTIONS = np.arange(9, dtype=np.int8)
CHECKS = np.array([
    [0, 1, 2], # rows
    [3, 4, 5],
    [6, 7, 8],

    [0, 3, 6], # columns
    [1, 4, 7],
    [2, 5, 8],

    [0, 4, 8], # diagnals
    [2, 4, 6]
], dtype=np.int8)

class Tictactoe(Game):
    def __init__(self):
        super().__init__()
    
    @property
    def current_player(self):
        return self._current_player

    @current_player.setter
    def current_player(self, value):
        self._current_player = value

    def setup(self):
        self.current_player = 1
        self.board = np.zeros(9, dtype=np.int8)

    def get_valid_actions(self):
        return ACTIONS[np.where(self.board==0)]

    def apply(self, action):
        # if action is invalid, give win to other player
        if self.board[action] != 0:
            return True, -self.current_player

        self.board[action] = self.current_player

        finished, winner = self.get_result()
        self.current_player = -self.current_player
    
        return finished, winner

    def get_result(self):
        # calculate array that shows which sqaures belong to current player
        player_board = self.board==self.current_player

        # check if current player has a 3-in-a-row
        for sqaures in CHECKS:
            if np.all(player_board[sqaures]):
                return True, self.current_player

        return np.all(self.board!=0), 0

    def __str__(self):
        return f'''
        {self.get_symbol(self.board[0])}|{self.get_symbol(self.board[1])}|{self.get_symbol(self.board[2])}
        -----
        {self.get_symbol(self.board[3])}|{self.get_symbol(self.board[4])}|{self.get_symbol(self.board[5])}
        -----
        {self.get_symbol(self.board[6])}|{self.get_symbol(self.board[7])}|{self.get_symbol(self.board[8])}
        '''

    def get_symbol(self, value):
        if value == 1:
            return 'X'
        elif value == -1:
            return 'O'
        else:
            return ' '