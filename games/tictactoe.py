from game import Game

import numpy as np

# sorted(list(permutations(range(3), 2)) + list(zip(range(3), range(3))))
ACTIONS = [
    (0,0),(1,0),(2,0),
    (0,1),(1,1),(2,1),
    (0,2),(1,2),(2,2)
]

class Tictactoe(Game):
    def setup(self):
        self.current_player = 1
        self.last_action = None
        self.board = np.zeros((3,3), dtype=np.int8)

    def actions(self):
        return ACTIONS

    def valid_actions(self):
        return [action for action in ACTIONS if self.board[action] == 0]

    def invalid_actions(self):
        return [action for action in ACTIONS if self.board[action] != 0]

    def apply(self, action):
        # if action is invalid, do nothing and let caller decide what to do
        if self.board[action] != 0:
            return False

        self.board[action] = self.current_player
        self.current_player = -self.current_player
        self.last_action = action

        return True

    def result(self):
        if self.last_action == None:
            return False, 0

        row, column = self.last_action
        previous_player = -self.current_player

        checks = [
            self.board[row, range(3)], # column
            self.board[range(3), column], # row
        ]

        if row == column:
            checks.append(self.board[range(3), range(3)]) # diagnal
        if 2 - row == column:
            checks.append(self.board[[2,1,0], range(3)]) # anti-diagnal

        for squares in checks:
            if np.all(squares == previous_player):
                return True, previous_player

        return np.all(self.board != 0), 0

    def heuristic(self):
        checks = [
            self.board[0, range(3)], # columns
            self.board[1, range(3)],
            self.board[2, range(3)],
            self.board[range(3), 0], # row
            self.board[range(3), 1],
            self.board[range(3), 2],
            self.board[range(3), range(3)], # diagnal
            self.board[[2,1,0], range(3)] # anti-diagnal
        ]

        opponent = -self.current_player

        total = 0
        for check in checks:
            player_count = np.count_nonzero(check == self.current_player)
            opponent_count = np.count_nonzero(check == opponent)

            # 100 for 3-in-a-row, 10 for 2-in-a-row, 1 for 1-in-a-row
            if opponent_count == 0 and player_count != 0:
                total += self.current_player * 10**(player_count-1)
            elif player_count == 0 and opponent_count != 0:
                total += opponent * 10**(opponent_count-1)
            
        return total / (len(checks) * 100) # limit result between -1 and 1

    def get_symbol(self, value):
        if value == 1:
            return 'X'
        elif value == -1:
            return 'O'
        else:
            return ' '

    def __str__(self):
        line = '|-----|\n'
        string = line

        for row in range(3):
            symbols = map(self.get_symbol, self.board[row])
            string += '|' + '|'.join(symbols) + '|\n'
            string += line

        return string

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