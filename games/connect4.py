'''
References:
https://github.com/denkspuren/BitboardC4/blob/master/BitboardDesign.md
https://www.gamedev.net/forums/topic/225611-connect-4-evaluation/
'''

from games import Game

from codetiming import Timer
import numpy as np

HEIGHT = 6
WIDTH = 7
COLUMNS = list(range(WIDTH))
MAGIC_NUMBERS = [1, 7, 6, 8] # used to check for vertical, horizontal, anit-diagonal, and diagonal 4-in-a-rows respectively

class Connect4(Game):
    def setup(self):
        # bitboard indicating player1 and player2's pieces respectively
        self.player1_board = 0
        self.player2_board = 0

        # the number of pieces that have been placed
        self.piece_count = 0

        # bottom most empty slots (as an index) for each column
        self.piece_heights = [0, 7, 14, 21, 28, 35, 42] # [0, 7, 15, 24, 30, 35, 42]

    def actions(self):
        return COLUMNS

    def valid_actions(self):
        return [column for column in COLUMNS if not self.is_full(column)]

    def invalid_actions(self):
        return [column for column in COLUMNS if self.is_full(column)]

    @profile
    def apply(self, column):
        # if action is invalid, do nothing and let caller decide what to do
        if self.is_full(column):
            return False

        # place piece in empty board in correct slot
        mask = 1 << self.piece_heights[column]

        # apply mask to current board
        if self.current_player == 1:
            self.player1_board ^= mask
        else:
            self.player2_board ^= mask

        self.piece_heights[column] += 1
        self.piece_count += 1

        return True

    @profile
    # @Timer('result', logger=None)
    def result(self):
        previous_player = -self.current_player
        if previous_player == 1:
            board = self.player1_board
        else:
            board = self.player2_board

        if self.is_4_in_row(board):
            return True, previous_player

        return self.piece_count == 42, 0

    @profile
    def heuristic(self):
        num_odd = 0 # of odd threats by player 2 minus # of odd threats by player 1
        num_mixed = 0 # of mixed odd threats
        num_even = 0 # of even threats by player 2

        for column in COLUMNS:
            start_index = self.piece_heights[column]+1
            row = start_index % 7

            if row == 0: # row is full
                continue

            # for each possible threat, check if threat
            for slot_index in range(start_index, start_index + (6-row)):
                mask = 1 << slot_index

                if row % 2 == 0: # odd row (account for zero indexing)
                    # place piece in slot
                    player1_board_copy = mask ^ self.player1_board
                    player2_board_copy = mask ^ self.player2_board

                    # see if placed piece causes 4-in-row
                    player1_4_in_row = self.is_4_in_row(player1_board_copy)
                    player2_4_in_row = self.is_4_in_row(player2_board_copy)

                    if player1_4_in_row and player2_4_in_row:
                        num_mixed += 1
                    elif player1_4_in_row:
                        num_odd -= 1
                    elif player2_4_in_row:
                        num_odd += 1
                else:
                    player2_board_copy = mask ^ self.player2_board
                    if self.is_4_in_row(player2_board_copy):
                        num_even += 1

        # return predicted result of game based of number of even, odd, and mixed threats
        if num_odd < 0:
            return 1
        elif num_odd == 0:
            if num_mixed % 2 != 0:
                return 1
            else:    
                if num_mixed==0:    
                    if num_even == 0:
                        return 0
                    else:
                        return -1      
                else:
                    return -1
        elif num_odd == 1:
            if num_mixed % 2 != 0:
                return -1
            else:
                return 1             
        else:
            return -1

    def __str__(self):
        board_array = self.board
        line = '|-------------|\n'
        string = line

        for row in range(HEIGHT):
            symbols = map(self.get_symbol, board_array[row])
            string += '|' + '|'.join(symbols) + '|\n'
            string += line

        return string

    def __hash__(self):
        return hash((self.player1_board << 49) + self.player2_board)

    def __eq__(self, other):
        return self.player1_board == other.player1_board and self.player2_board == other.player2_board

    def get_symbol(self, value):
        if value == 1:
            return 'X'
        elif value == -1:
            return 'O'
        else:
            return ' '

    def is_4_in_row(self, board):
        for num in MAGIC_NUMBERS:
            # align all 4-in-a-rows together based on magic number then 'and' their values together
            temp = board & (board >> num)
            if temp & (temp >> 2 * num) != 0:
                return True

        return False

    def is_full(self, column):
        # works as extra row starts at 6 and has a differance of 7
        return self.piece_heights[column] % 7 == 6 # self.piece_heights[column]-6) % 7 != 0

    @property
    def current_player(self):
        return 1 if self.piece_count % 2 == 0 else -1

    @property
    def board(self):
        player1_board_copy = self.player1_board
        player2_board_copy = self.player2_board
        board_array = np.zeros((HEIGHT, WIDTH), dtype=np.int8)

        for index in range(49):
            # get numpy array column (columns to the right have higher numbers) and row (lower rows have higher numbers)
            # from bitboard index (starts at bottom left and increases upward)
            col = index // 7 # as the bottom of each column is a multiple of 7
            row = 5 - (index % 7)

            if row != -1: # if index is not apart of extra row
                if player1_board_copy & 1 == 1:
                    board_array[row][col] = 1
                elif player2_board_copy & 1 == 1:
                    board_array[row][col] = -1

            player1_board_copy = player1_board_copy >> 1
            player2_board_copy = player2_board_copy >> 1

        return board_array
