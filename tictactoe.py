from game import Game
import numpy as np

class TicTacToe(Game):
    def __init__(self, player1, player2, starting_player=1):
        super().__init__(player1, player2)

        self.current_player = starting_player
        self.board = np.zeros((3, 3), dtype=np.byte)
        self.last_action = None # (row, column)

    def move(self):
        if self.current_player == 1:
            action = self.player1.act(self.board)
        else:
            action = self.player2.act(self.board)

        if self.board[action] == 0:
            self.board[action] = self.current_player

        self.last_action = action

    def is_finished(self):
        checks = [
            self.board[self.last_action[0], range(3)], # column
            self.board[range(3), self.last_action[1]], # row
        ]

        if self.last_action[0] == self.last_action[1]:
            checks.append(self.board[range(3), range(3)]) # diagnal
        if 2 - self.last_action[0] == self.last_action[1]:
            checks.append(self.board[reversed(range(3)), range(3)]) # anti-diagnal

        for squares in checks:
            if all(x == self.current_player for x in squares):
                return True, self.current_player

        return all(x != 0 for x in self.board.nditer), 0

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