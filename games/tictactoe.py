from game import Game

import numpy as np

HEIGHT = 3
WIDTH = 3
POSITIONS = list(range(HEIGHT*WIDTH))

'''
0|1|2
-----
3|4|5
-----
6|7|8
'''

CHECKS = [
    0b000000111, # horizontals
    0b000111000,
    0b111000000,
    0b001001001, # verticals
    0b010010010,
    0b100100100,
    0b001010100, # diagnal
    0b100010001, # anti-diagnal
]

class Tictactoe(Game):
    def setup(self):
        # bitboard indicating player1 and player2's pieces respectively
        self.player1_board = 0
        self.player2_board = 0

        # the number of pieces that have been placed
        self.piece_count = 0

    def actions(self):
        return POSITIONS

    def valid_actions(self):
        return [position for position in POSITIONS if self.is_empty(position)]

    def invalid_actions(self):
        return [position for position in POSITIONS if not self.is_empty(position)]

    def apply(self, position):
        # if action is invalid, do nothing and let caller decide what to do
        if not self.is_empty(position):
            return False

        mask = 1 << position
        if self.current_player == 1:
            self.player1_board |= mask
        else:
            self.player2_board |= mask

        self.piece_count += 1

        return True

    def result(self):
        for check in CHECKS:
            if self.player1_board & check == check:
                return True, 1
            elif self.player2_board & check == check:
                return True, -1

        return self.piece_count == 9, 0

    def heuristic(self):
        result = 0
        for check in CHECKS:
            count1 = bin(self.player1_board & check).count('1')
            count2 = bin(self.player2_board & check).count('1')
            
            if count1 != 0 and count2 == 0:
                result += 10**count1
            elif count2 != 0 and count1 == 0:
                result -= 10**count2

        return result

    def get_symbol(self, value):
        if value == 1:
            return 'X'
        elif value == -1:
            return 'O'
        else:
            return ' '

    def is_empty(self, position):
        mask = 1 << position
        return self.player1_board & mask == 0 and self.player2_board & mask == 0

    def __str__(self):
        line = '|-----|\n'
        string = line
        board_array = self.board.reshape((3,3))

        for row in range(HEIGHT):
            symbols = map(self.get_symbol, board_array[row])
            string += '|' + '|'.join(symbols) + '|\n'
            string += line

        return string

    @property
    def current_player(self):
        return 1 if self.piece_count % 2 == 0 else -1

    @property
    def board(self):
        player1_board_copy = self.player1_board
        player2_board_copy = self.player2_board
        board_array = np.zeros((HEIGHT * WIDTH), dtype=np.int8)

        for position in POSITIONS:
            if player1_board_copy & 1 == 1 or player2_board_copy & 1 == 1:
                board_array[position] = 1

            player1_board_copy = player1_board_copy >> 1
            player2_board_copy = player2_board_copy >> 1

        return board_array