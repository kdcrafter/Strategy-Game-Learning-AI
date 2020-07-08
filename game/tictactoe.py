# from game import Game
import numpy as np
from numba import njit

class TictactoeGame("""AbstractGame"""):
    def __init__(self, player1, player2, starting_player=1):
        super().__init__(player1, player2)

        self.current_player = starting_player
        self.board = np.zeros((3, 3), dtype=np.int8)
        self.last_action = None # (row, column)

    def move(self):
        if self.current_player == 1:
            action = self.player1.act(self.board)
        else:
            action = self.player2.act(self.board)

        if self.board[action] == 0:
            self.board[action] = self.current_player
            self.last_action = action
            return True
        else:
            return False

    def is_finished(self):
        checks = [
            self.board[self.last_action[0], range(3)], # column
            self.board[range(3), self.last_action[1]], # row
        ]

        if self.last_action[0] == self.last_action[1]:
            checks.append(self.board[range(3), range(3)]) # diagnal
        if 2 - self.last_action[0] == self.last_action[1]:
            checks.append(self.board[[2, 1, 0], range(3)]) # anti-diagnal

        for squares in checks:
            if all(x == self.current_player for x in squares):
                return True, self.current_player

        return all(x != 0 for x in np.nditer(self.board)), 0

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

TICTACTOE_ACTIONS = np.arange(9, dtype=np.int8)

class TictactoeState():
    # TODO: check if copy should be done here
    def __init__(self, current_player, board = np.zeros(9, dtype=np.int8)):
        self.current_player = current_player
        self.board = board
        self.last_action = None

    @njit
    def get_valid_actions(self):
        return TICTACTOE_ACTIONS[np.where(TICTACTOE_ACTIONS==0)]

    # TODO: after tictactie game is implemented
    def get_result(self):
        pass
        # #check if previous move caused a win on vertical line 
        # if board[0][y] == board[1][y] == board [2][y]:
        #     return True

        # #check if previous move caused a win on horizontal line 
        # if board[x][0] == board[x][1] == board [x][2]:
        #     return True

        # #check if previous move was on the main diagonal and caused a win
        # if x == y and board[0][0] == board[1][1] == board [2][2]:
        #     return True

        # #check if previous move was on the secondary diagonal and caused a win
        # if x + y == 2 and board[0][2] == board[1][1] == board [2][0]:
        #     return True

        # return False 

        # return all(x != 0 for x in np.nditer(self.board)), 0

    # TODO: after tictactie game is implemented
    def apply(self, action):
        pass
        # if self.current_player == 1:
        #     action = self.player1.act(self.board)
        # else:
        #     action = self.player2.act(self.board)

        # if self.board[action] == 0:
        #     self.board[action] = self.current_player
        #     self.last_action = action
        #     return True
        # else:
        #     return False

    def show(self):
        pass