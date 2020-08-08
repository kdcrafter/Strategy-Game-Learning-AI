from games import Game

import numpy as np

HEIGHT = 6
WIDTH = 7
ACTIONS = list(range(WIDTH))

class Connect4(Game):
    def setup(self):
        self.current_player = 1
        self.last_slot = None
        self.board = np.zeros((HEIGHT,WIDTH), dtype=np.int8)

    def actions(self):
        return ACTIONS

    def valid_actions(self):
        return [action for action in ACTIONS if self.board[0,action] == 0]

    def invalid_actions(self):
        return [action for action in ACTIONS if self.board[0,action] != 0]

    def apply(self, action):
        # if action is invalid, do nothing and let caller decide what to do
        if self.board[0, action] != 0:
            return False

        # get index of the last empty slot in the to be placed column
        column = self.board[:,action]
        index = np.where(column == 0)[0][-1]
        self.board[index,action] = self.current_player
        
        # switch current_player at start of apply() ?
        self.current_player = -self.current_player

        self.last_slot = (index, action) # (row, column)

        return True

    def result(self):
        if self.last_slot == None:
            return False, 0

        row, col = self.last_slot
        previous_player = -self.current_player

        # get slots above and below the last slot
        updown = self.board[:,col]
        up = np.flip(updown[:row])
        down = updown[row+1:]

        # get slots to the left and right of the last slot
        leftright = self.board[row,:]
        left = np.flip(leftright[:col])
        right = leftright[col+1:]

        # get slots to the top right and bottom left of the last slot
        offset = col - row
        pos_offset = max(offset, 0)
        diag = self.board.diagonal(offset)
        upper_diag = np.flip(diag[:col-pos_offset])
        lower_diag = diag[col-pos_offset+1:]

        # get slots to the top left and bottom right of the last slot
        flipped_col = WIDTH-1-col
        flipped_board = np.fliplr(self.board)
        offset = flipped_col - row
        pos_offset = max(offset, 0)
        anti_diag = flipped_board.diagonal(offset)
        upper_anti_diag = np.flip(anti_diag[:flipped_col-pos_offset])
        lower_anti_diag = anti_diag[flipped_col-pos_offset+1:]

        checks = [
            (up, down),
            (left, right),
            (upper_diag, lower_diag),
            (upper_anti_diag, lower_anti_diag)
        ]

        for upper_check, lower_check in checks:
            upper_count = 0
            for slot in upper_check:
                if slot == previous_player:
                    upper_count += 1
                else:
                    break

            lower_count = 0
            for slot in lower_check:
                if slot == previous_player:
                    lower_count += 1
                else:
                    break

            if upper_count + lower_count >= 4:
                return True, previous_player

        return np.all(self.board != 0), 0

    def heuristic(self):
        total = 0
        num_checks = 0

        # total possible horizontal arrays
        for row in range(HEIGHT):
            for start_col in range(WIDTH-4+1): # cols 0 through 3
                num_checks += 1
                array = self.board[row,start_col:start_col+4]
                total += self.get_array_heuristic(array)

        # total possible vertical arrays
        for col in range(WIDTH):
            for start_row in range(HEIGHT-4+1): # rows 0 through 2
                num_checks += 1
                array = self.board[start_row:start_row+4,col]
                total += self.get_array_heuristic(array)

        # total possible diagonal arrays
        for i in range(-2, 3+1): # to get all diagonals with len >= 4
            diag = self.board.diagonal(i)
            for j in range(len(diag)-4+1):
                num_checks += 1
                array = diag[j:j+4]
                total += self.get_array_heuristic(array)

        # total possible anti diagonal arrays
        flipped_board = np.fliplr(self.board)
        for i in range(-2, 3+1): # to get all anti diagonals with len >= 4
            anti_diag = flipped_board.diagonal(i)
            for j in range(len(anti_diag)-4+1):
                num_checks += 1
                array = anti_diag[j:j+4]
                total += self.get_array_heuristic(array)

        return total / (num_checks * 1000) # limit result between -1 and 1

    def get_array_heuristic(self, array):
        player_count = np.count_nonzero(array == self.current_player)
        opponent_count = np.count_nonzero(array == -self.current_player)

        # 1000 for 4-in-a-row, 100 for 3-in-a-row, ...
        if opponent_count == 0  and player_count != 0:
            return self.current_player * 10**(player_count-1)
        elif player_count == 0 and opponent_count != 0:
            return -self.current_player * 10**(opponent_count-1)
        else:
            return 0

    def get_symbol(self, value):
        if value == 1:
            return 'X'
        elif value == -1:
            return 'O'
        else:
            return ' '

    def __str__(self):
        line = '|-------------|\n'
        string = line

        for row in range(HEIGHT):
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