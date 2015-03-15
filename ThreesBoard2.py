########################################################################
# TILES AND DECK RELATED
########################################################################

_BASE_DECK = [
    1, 1, 1, 1,
    2, 2, 2, 2,
    3, 3, 3, 3
]

def _draw_tile(deck):
    """Draw tile from deck without replacement"""

    try:
        tile = choice(deck)
    except IndexError:
        deck = _BASE_DECK
        tile = choice(deck)
    
    deck.remove(tile)
    
    return tile, deck

########################################################################
# BOARD CREATION RELATED
########################################################################

def _populate_board(board, deck, num_of_tiles):
    """Put initial tiles on the board"""

    size = len(board)

    for i in range(num_of_tiles):
        tile = deck.get_next_tile()

        # Place tiles randomly on the board
        while True:
            pos = int(ceil(size**2 * random())) - 1
            x = pos / size
            y = pos % size

            if board[x][y] == 0:
                board[x][y] = tile
                break

    return board, deck

def _init_board(n, m):
    """Create a n x n sized board, and filled it with m tiles
    
    Return the filled board, and left over tiles from unfinished deck"""

    if m > n ** 2:
        raise InitBoardTileNumberError

    else:

        board = [[0] * n for x in xrange(n)]
    
        deck = _BASE_DECK[:]
    
        return _populate_board(board, deck, m)


########################################################################
# SWIPE RELATED
########################################################################

def _reverse(board):
    """Reverse the board right and left"""

    for row in board:
        row.reverse()

    return board


def _row2col(board):
    """Reflect across the diagonal"""

    new_board = board[:]  # make a new copy of the grid

    size = len(board)

    for x in range(size):
        for y in range(x):
            new_board[y][x], board[x][y] = board[x][y], new_board[y][x]

    return new_board


def _shift_left(row):
    """Performs what happen at row level when you swipe left in Threes

    Adding next tile does not happen at this level.
    """

    for i in range(1, len(row)):

        # Move tile left if the left space is empty
        if row[i-1] == 0:
            row[i-1], row[i] = row[i], row[i-1]

        # Merge left, if the two tiles are the same, and divisible by 3
        elif row[i-1] == row[i] and row[i] % 3 == 0:
            row[i-1] *= 2
            row[i] = 0

        # Merge left, if two tiles adds up to 3
        elif row[i-1] + row[i] == 3:
            row[i-1] = 3
            row[i] = 0

    return row


def _swipe_left(board, tile=0):
    """Perform what happens at board level when you swipe left

    Adds the next tile
    Add no tile by default
    """

    copy_board = deepcopy(board)

    for row in copy_board:
        row = _shift_left(row)

    if copy_board == board:
        return board

    else:
        # Add next tile
        while True:
            pick = randint(0, len(board) - 1)

            if board[pick] != copy_board[pick]:
                copy_board[pick][-1] = tile
                break

        return copy_board


def _swipe_right(board, tile):
    """Perform what happens at board level when you swipe right

    Based on _swipe_left
    """

    return _reverse(_swipe_left(_reverse(board), tile))


def _swipe_up(board, tile):
    """Perform what happens at board level when you swipe up

    Based on _swipe_left
    """

    return _row2col(_swipe_left(_row2col(board), tile))


def _swipe_down(board, tile):
    """Perform what happens at board level when you swipe down

    Based on _swipe_left
    """

    return _row2col(_swipe_right(_row2col(board), tile))

########################################################################
# Exceptions 
########################################################################


class NoMovementError:
    pass


class TooManyTilesError:
    pass


class InValidMoveError:
    pass

class EmptyDeckError:
    pass

class InitBoardTileNumberError:
    pass


########################################################################
# THREES BOARD CLASS
########################################################################

from copy import deepcopy

class ThreesBoard(object):

    def __init__(self, size=4, starting_tiles=9, history=[]):
    
        if history:
            self.history = history
            self.board = history[-1][1]
            self.deck = history[-1][2]
            self.next_tile = history[-1][3]
        
        else:
            self.board, self.deck = init_deck(size, starting_tiles)
            self.next_tile, self.deck = _draw_tile(self.deck)
            self.history = [('start', self.board, 
                             self.deck, self.next_tile)]
        
    def swipe(self, move):

        direction = {'left': _swipe_left,
                     'right': _swipe_right,
                     'up': _swipe_up,
                     'down': _swipe_down}

        copy_board = deepcopy(self.board)

        try:
            copy_board = direction[move](copy_board, self.nextTile)

        except KeyError:
            raise InValidMoveError

        if self.board == copy_board:
            # raise NoMovementError
            pass

        else:
            self.board = copy_board
            self.highestTile = _get_highest(self.board)
            self.nextTile = self.deck.get_next_tile(self.highestTile)

            # Histoyr formate is: move, resulting board, next tile
            self.history.append((move, self.board, self.nextTile))

########################################################################
# UNIT TESTING
########################################################################

###########
# Imports #
###########

import unittest
from random import choice


#######################
# Important Constants #
#######################

ALL_MOVE_VALUES = (
    'start', 'left', 'right', 'up', 'down', 'end'
)

ALL_BOARD_CELL_VALUES = (
    0, 1, 2, 3, 6, 12, 24, 48, 96, 192, 384, 768, 1536, 3072, 6144
)

ALL_DECK_TILE_VALUES = (1, 2, 3)

ALL_BONUS_DECK_VALUES = (
    [],
    [6],
    [6, 12],
    [6, 12, 24],
    [12, 24, 48],
    [24, 48, 96],
    [48, 96, 192],
    [96, 192, 384],
    [192, 384, 768]
)

ALL_NEXT_TILE_VALUES = (ALL_DECK_TILE_VALUES, ALL_BONUS_DECK_VALUES)

#############
# Test Case #
#############

class ThreesBoardTest(unittest.TestCase):

    def setUp(self):
        all_moves = ('left', 'right', 'up', 'down')
        test_game = ThreesBoard()

        while True:
   
            while not test_game.game_over():
                test_game.swipe(choice(all_moves))
            
            if test_game.highest_tile == 96:
                break
            
            else:
                test_game = ThreesBoard()

        self.history = test_game.history
        self.board = self.history[-1][1]
        self.deck = self.history[-1][2]
        self.bonus_deck = self.history[-1][3]

    def test_start_game(self):
        assert self.history[0][0] == 'start'
        
    def test_end_game(self):
        assert self.history[-1][0] == 'end'
    
    def test_board_valid_size(self):
        size = len(self.board)
        for row in self.board:
            assertEqual(len(row), size)
            
    def test_board_valid_tiles(self):
        all_tiles = [tile for sublist in self.board for tile in sublist]
        tiles = set(all_tiles)
        assert tiles.issubset(ALL_BOARD_CELL_VALUES)
        
    def test_deck_valid_tiles(self):
        tiles = set(self.deck)
        assert tiles.issubset(ALL_DECK_TILE_VALUES)
        
    def test_bonus_deck_used(self):
        bonus_deck_used = []
        for turn in self.history:
            bonus_deck_used.append(turn[3])
        bonus_decks = set(bonus_deck_used)
        assert bonus_deck.issubset(ALL_BONUS_DECK_VALUES)
        
    def test_board_history
            
########################################################################
# Main
########################################################################

if __name__ == "__main__":
        
    unittest.main()


