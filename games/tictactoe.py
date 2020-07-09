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
    def __init__(self, current_player=1, board=None):
        super().__init__(current_player=current_player, board=board)
        self.setup(current_player=current_player, board=board)

    def setup(self, current_player=1, board=None):
        self.current_player = current_player

        if board is None:
            self.board = np.zeros(9, dtype=np.int8)
        else:
            self.board = board

    def get_valid_actions(self):
        return ACTIONS[np.where(self.board==0)]

    def get_result(self):
        # calculate array that shows which sqaures belong to player who made the last move
        previous_player = -self.current_player
        player_board = self.board==previous_player

        # check if previous player has a 3-in-a-row
        for sqaures in CHECKS:
            if np.all(player_board[sqaures]):
                return True, previous_player

        return np.all(self.board!=0), 0

    def get_copy(self):
        return Tictactoe(self.current_player, np.copy(self.board))

    def get_symbol(self, value):
        if value == 1:
            return 'X'
        elif value == -1:
            return 'O'
        else:
            return ' '

    def apply(self, action):
        # if action is invalid, do nothing and let caller decide what to do
        if self.board[action] != 0:
            return False

        self.board[action] = self.current_player
        self.current_player = -self.current_player

        return True

    def __str__(self):
        return f'''
        {self.get_symbol(self.board[0])}|{self.get_symbol(self.board[1])}|{self.get_symbol(self.board[2])}
        -----
        {self.get_symbol(self.board[3])}|{self.get_symbol(self.board[4])}|{self.get_symbol(self.board[5])}
        -----
        {self.get_symbol(self.board[6])}|{self.get_symbol(self.board[7])}|{self.get_symbol(self.board[8])}
        '''

    @property
    def current_player(self):
        return self._current_player

    @current_player.setter
    def current_player(self, value):
        self._current_player = value

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, value):
        self._board = value