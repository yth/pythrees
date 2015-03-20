###########

# Imports #

###########


from random import choice
from copy import deepcopy


######################################

# TILES, DECK and BONUS_DECK RELATED #

######################################


_BASE_DECK = [
    1, 1, 1, 1,
    2, 2, 2, 2,
    3, 3, 3, 3
]


def _draw_tile(deck):
    try:
        tile = [choice(deck)]
    except IndexError:
        deck = _BASE_DECK[:]
        tile = [choice(deck)]

    deck.remove(tile[0])

    return tile, deck


def _get_highest_tile(board):
    """Use max() on a flattened board to get highest valued tile"""

    return max([tile for row in board for tile in row])


def _create_bonus_deck(base=0):
    return filter(lambda x: x >= 6, [base / 32, base / 16, base / 8])


##########################

# BOARD CREATION RELATED #

##########################


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
                board[x][y] = choice(tile)
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


#################

# SWIPE RELATED #

#################


def _reverse(board):
    for row in board:
        row.reverse()
    return board


def _row2col(board):
    for x in range(len(board)):
        for y in range(x):
            board[x][y], board[y][x] = board[y][x], board[x][y]
    return board


def _shift_left(row):
    """Row level swipe left"""

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

    Adds the next tile or an empty space
    """

    copy_board = deepcopy(board)

    for row in copy_board:
        row = _shift_left(row)

    if copy_board == board:
        return board

    else:
        # Add a tile or space
        picks = []
        
        for row in range(len(board)):
            if board[row] != copy_board[row]:
                picks.append(row)

        pick = choice(picks)
        copy_board[pick][-1] = tile


        return copy_board


def _swipe_right(board, tile):
    return _reverse(_swipe_left(_reverse(board), tile))


def _swipe_up(board, tile):
    return _row2col(_swipe_left(_row2col(board), tile))


def _swipe_down(board, tile):
    return _row2col(_swipe_right(_row2col(board), tile))


##############

# Exceptions #

##############


class InValidMoveError:
    pass


class InitBoardTileNumberError:
    pass


#######################

# THREES ENGINE CLASS #

#######################


class ThreesEngine(object):

    def __init__(self, size=4, starting_tiles=9, history=[]):
    
        assert isinstance(history, list)

        if history:
            self.history = history
            self.board = eval(history[-1][1])
            self.deck = eval(history[-1][2])
            self.next_tile = eval(history[-1][3])
            self.highest_tile = _get_highest_tile(self.board)

        else:

            self.board, self.deck = _init_board(size, starting_tiles)
            self.next_tile, self.deck = _draw_tile(self.deck)
            self.history = [('start', repr(self.board),
                             repr(self.deck), repr(self.next_tile))]
            self.highest_tile = _get_highest_tile(self.board)

    def swipe(self, move):

        direction = {'left': _swipe_left,
                     'right': _swipe_right,
                     'up': _swipe_up,
                     'down': _swipe_down}

        copy_board = deepcopy(self.board)

        try:
            copy_board = direction[move](copy_board, 
                                         choice(self.next_tile))

        except KeyError:
            raise InValidMoveError

        if self.board != copy_board:
            self.board = copy_board
            self.highest_tile = _get_highest_tile(self.board)
            self.next_tile, self.deck = _draw_tile(self.deck)
            self.history.append((move, repr(self.board),
                                 repr(self.deck), repr(self.next_tile)))

    def game_over(self):
        new_board = deepcopy(self.board)

        if (_swipe_left(new_board, 0) == self.board and
                _swipe_right(new_board, 0) == self.board and
                _swipe_up(new_board, 0) == self.board and
                _swipe_down(new_board, 0) == self.board):
            return True
        return False


if __name__ == "__main__":

    print 'Threes Engine Module'
    
    game = ThreesEngine()
    print game.board
    
    while not game.game_over():
        move = choice(['left', 'right', 'up', 'down'])
        game.swipe(move)
    
    for row in game.board:
        print row
    
    print '--- --- ---'
    
    for turn in game.history:
        print turn[0]
        for row in eval(turn[1]):
            print row
        print ''
        
    print len(game.history)
