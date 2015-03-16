from random import choice, randint
from copy import deepcopy
from math import ceil

########################################################################
# TILES, DECK and BONUS_DECK RELATED
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
        deck = _BASE_DECK[:]
        tile = choice(deck)
    
    deck.remove(tile)
    
    return tile, deck

def _get_highest_tile(board):
    highest_tile = 0
    
    for row in board:
        for tile in row:
            if tile > highest_tile:
                highest_tile = tile
    
    return highest_tile

def _create_bonus_deck(self, test=0)
        pass
        # bonus_deck = filter(>= 6, [base / 32, base / 16, base / 8])
        
    def _

########################################################################
# BOARD CREATION RELATED
########################################################################

def _populate_board(board, deck, num_of_tiles):
    """Put initial tiles on the board"""

    n = len(board)

    for i in range(num_of_tiles):
        tile, deck = _draw_tile(deck)

        # Place tiles randomly on the board
        # Create a list of range(n ** 2), and shuffle
        # Then place one by one
        while True:
            pos = choice(range(n ** 2))
            x = pos / n
            y = pos % n

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
    for row in board:
        row.reverse()
    return board


def _row2col(board):
    new_board = board[:]

    size = len(board)

    # TO DO: Experiment with just using one board
    for x in range(size):
        for y in range(x):
            new_board[y][x], board[x][y] = board[x][y], new_board[y][x]

    return new_board


def _shift_left(row):
    """
    Performs what happen at row level when you swipe left in Threes
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
    Add empty spaces by default
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
# THREES ENGINE CLASS
########################################################################

class ThreesEngine(object):

    def __init__(self, size=4, starting_tiles=9, history=[]):
    
        if history:
            self.history = history
            self.board = history[-1][1]
            self.deck = history[-1][2]
            self.next_tile = history[-1][3]
            self.highest_tile = _get_highest_tile(self.board)
        
        else:
            self.board, self.deck = _init_board(size, starting_tiles)
            self.next_tile, self.deck = _draw_tile(self.deck)
            self.history = [('start', self.board, 
                             self.deck, self.next_tile)]
            self.highest_tile = _get_highest_tile(self.board)
    

    
    
    '''
    def swipe(self, move):

        direction = {'left': _swipe_left,
                     'right': _swipe_right,
                     'up': _swipe_up,
                     'down': _swipe_down}

        copy_board = deepcopy(self.board)

        try:
            copy_board = direction[move](copy_board, self.next_tile)

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

    def game_over(self):
        new_board = deepcopy(self.board)

        if (_swipe_left(new_board, 0) == self.board and
                _swipe_right(new_board, 0) == self.board and
                _swipe_up(new_board, 0) == self.board and
                _swipe_down(new_board, 0) == self.board):
            return True
        return False
'''

if __name__ == "__main__":
    '''
    from string import center
    
    test = ThreesEngine()
    
    while not test.game_over():
        move = choice(['left', 'right', 'up', 'down'])
        test.swipe(move)
        
    for row in test.board:
        for tile in row:
            print center(str(tile), 6, ' '),
        print ''
    '''
    
    test = ThreesEngine()
    
    print test.history
