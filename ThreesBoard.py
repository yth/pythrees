########################################################################
# Threes! is a game by by Asher Vollmer, Greg Wohlwend, Jimmy Hinson,  #
# and Hidden Variable. This is created so that AI/ML strategies for    #
# the game can be developed and tested easier, and is not intended as  #
# a replacement of the original game. Please support the developers by #
# purchasing their excellent game!                                     #
########################################################################


""" This is the Threes Board class.

The board creation, game logic and record keeping are all in this file.
For testing AI strategy with Threes, you probably only need this.
"""


###########
# Imports #
###########


from __future__ import print_function


import random
import copy


from TileDeck import TileDeck


##############
# Exceptions #
##############

# Raise this error if the board did not change after a swipe
class NoMovementError:
    pass


# Raise this error if found out trying to place to many tiles on board
# during the initialization of the board
class TooManyTilesError:
    pass


# Raise this error if found trying to move in a direction not allowed
class InvalidMoveError:
    pass


###########################################
# Helper functions for creating the board #
###########################################

def _create_board(size=4):
    """Generating the empty starting game board

    This board can be of any (nxn) size.
    0 = a space with no tile
    """

    return [[0 for j in range(size)] for i in range(size)]

# Should add in the comments why the deck is returned as well.
def _populate_board(board, deck, nTiles):
    """Put the starting tiles on the board

    board - a list of list filled with 0's a la above function
    deck - Threes! does not use random decks, see TileDeck.py
    nTiles - determines how many tiles are used to populate board

    Remaining tiles are returned to be used in the game.
    """

    size = len(board)

    # nTiles is one factor that I want to experiment with. This is a
    # basic sanity check. You can't place more tiles on the board than
    # there are spaces
    if nTiles > size**2:
        # nTiles = size**2 ## If choose to silently resolve error
        raise TooManyTilesError

    positions = [(x, y) for x in range(size) for y in range(size)]
    random.shuffle(positions)

    for i in range(nTiles):
        tile = deck.get_next_tile()

        # Place tiles randomly on the board
        board[positions[i][0]][positions[i][1]] = tile
    
    return board, deck


####################################
# Helper function for board swipes #
####################################


def _shift_left(row):
    """Performs what happen at row level when you swipe left in Threes

    Adding next tile does not happen at this level.

    This is the fundamental operation of the board. All other behaviors
    are based on this one.
    """

    row_copy = copy.copy(row)

    for i in range(1, len(row_copy)):

        # Move tile left if the left space is empty
        if row_copy[i-1] == 0:
            row_copy[i-1], row_copy[i] = row_copy[i], row_copy[i-1]

        # Merge left, if the two tiles are the same, and divisible by 3
        elif row_copy[i-1] == row_copy[i] and row_copy[i] % 3 == 0:
            row_copy[i-1] *= 2
            row_copy[i] = 0

        # Merge left, if two tiles adds up to 3
        elif row_copy[i-1] + row_copy[i] == 3:
            row_copy[i-1] = 3
            row_copy[i] = 0

    return row_copy, 0 if row == row_copy else 1


def _swipe_left(board, tile=0):
    """Perform what happens at board level when you swipe left

    Adds the next tile
    Add no tile by default; tile=0, which is the empty tile
    """

    size = len(board)
    new_board = []
    changes = []
    bonus = isinstance(tile, list)

    for row in board:
        new_row, change = _shift_left(row)
        new_board.append(new_row)
        changes.append(change)

    # If the board did not change, then it's not a legal move
    if sum(changes) == 0:
        return board

    else:
        # Add next tile on a row that changed
        while True:
            pick = random.randint(0, size - 1)

            if changes[pick] == 0:
                continue

            else:
                new_board[pick][-1] = tile if not bonus else random.choice(tile)
                return new_board


def _swipe_right(board, tile=0):
    """Perform what happens at board level when you swipe right

    Based on _swipe_left
    """

    return _reverse(_swipe_left(_reverse(board), tile))


def _swipe_up(board, tile=0):
    """Perform what happens at board level when you swipe up

    Based on _swipe_left
    """

    return _row2col(_swipe_left(_row2col(board), tile))


def _swipe_down(board, tile=0):
    """Perform what happens at board level when you swipe down

    Based on _swipe_left
    """

    return _row2col(_swipe_right(_row2col(board), tile))


# I should move _reverse and _row2col below _swipe_left
def _reverse(board):
    """Reverse the board right and left"""

    new_board = copy.deepcopy(board)

    for row in new_board:
        row.reverse()

    return new_board


def _row2col(board):
    """Reflect across the "y=x" diagonal"""

    size = len(board)
    new_board = copy.deepcopy(board)

    for x in range(size):
        for y in range(x):
            new_board[y][x], new_board[x][y] = new_board[x][y], new_board[y][x]

    return new_board


########################
# Helper Function MISC #
########################


def _get_highest(board):
    """Return highest tile on the board, the board is a list of list

    Since the board unordered, you have to go through every element.
    """

    return max([val for row in board for val in row])


######################
# Threes Board Class #
######################


class ThreesBoard(object):
    """Captures everything about the game of Threes!

    It holds the board, tiles, and state of the game.
    It defines what are the allowable changes to the state.
    """

    def __init__(
            self,
            size=4,  # standard Threes board size, do more with it later
            nTiles=9,  # standard Threes number of starting tiles
            board=None,  # None or previous board
            deck=None,  # None, or previous deck
            history=None,  # None, or previous history
            nextTile=0):  # no tile, or previous tile

        """Creating the Threes board

        If passing in an old board position, that game will be recreated
        The tile deck will can also be recreated
        """

        if board:
            """To consider: store all information in history
                            eliminate the need for old boards, decks ...
                            initialize a previous game in form of
                            board = history[1]
                            nextTile = history[2]
                            ... etc
                            For next major version?
            """

            # Passing in the old game; size, ntiles are all ignored
            self.board = board
            self.deck = deck # Need to check whether this is None
            self.history = history
            self.highestTile = _get_highest(self.board)

            # If old game information was incomplete
            if nextTile == 0:
                self.nextTile = self.deck.get_next_tile(0)

            else:
                self.nextTile = nextTile

        else:
            # Starting a new game; ignore previous history ... etc
            self.board = _create_board(size)
            self.deck = TileDeck()

            # Populating a new board with start up tiles
            self.board, self.deck = _populate_board(self.board,
                                                   self.deck,
                                                   nTiles)

            self.nextTile = self.deck.get_next_tile()

            # Set up empty history, then set initial condition
            self.history = []

            # history formate is: move, resulting board, next tile)
            self.history.append(('start', self.board, self.nextTile))
            self.highestTile = 3

    def swipe(self, move):
        """Same function for different swipes

        This will make recording keeping easier
        """

        direction = {'left': _swipe_left,
                     'right': _swipe_right,
                     'up': _swipe_up,
                     'down': _swipe_down}

        copy_board = copy.deepcopy(self.board)

        try:
            copy_board = direction[move](copy_board, self.nextTile)

        except KeyError:
            raise InvalidMoveError

        if self.board != copy_board:
            self.board = copy_board
            self.highestTile = _get_highest(self.board)
            self.nextTile = self.deck.get_next_tile(self.highestTile)
            self.history.append((move, self.board, self.nextTile))

    def get_valid_moves(self):
        new_board = copy.deepcopy(self.board)
        moves = []
        if _swipe_left(new_board) != self.board:
            moves.append("left")
        if _swipe_right(new_board) != self.board:
            moves.append("right")
        if _swipe_up(new_board) != self.board:
            moves.append("up")
        if _swipe_down(new_board) != self.board:
            moves.append("down")
        return moves

    def gameOver(self):
        new_board = copy.deepcopy(self.board)

        return True if len(self.get_valid_moves()) == 0 else False

    def __eq__(self, other):
		# Consider add a check to history
        return (self.board == other.board and
                self.deck == other.deck and
                self.nextTile == other.nextTile)


if __name__ == "__main__":

        # Consider using a Python builtin testing framework

    # Testing on generating correct instances of games

    # test_board = [[1, 2, 3],
    #              [2, 3, 1],
    #              [3, 1, 2]]

    # test_deck = TileDeck([1,2,3])

    # test_history = ['start', test_board, 1]

    # game1 = ThreesBoard()
    # assert len(game1.board) == 4

    # game2 = ThreesBoard(5)
    # assert len(game2.board) == 5

    # game3 = ThreesBoard(5, 25)
    # assert len(game3.board) == 5
    # for row in game3.board:
    #    assert 0 not in row
    # assert len(game3.deck.deck) == 22

    # game4 = ThreesBoard(5, 25, test_board)
    # assert len(game4.board) == 3

    # game5 = ThreesBoard(4, 9, [], TileDeck([1,2,3]), test_history)
    # assert len(game5.deck.deck) == 14

    # game6 = ThreesBoard(4, 9, test_history[1],
    #                     TileDeck([1,2,3], test_history))
    # assert len(game6.board) == 3

    # Automated Play Test with Random Strategy
    from random import choice

    a = ThreesBoard()

    while not a.gameOver():
        moves = {'w': 'up',
                 'a': 'left',
                 's': 'down',
                 'd': 'right'}

        try:
            move = choice(list(moves.keys()))
            a.swipe(moves[move])

        except NoMovementError:
            pass

    print("\n  The next tile is :", a.nextTile, '\n')
    for row in a.board:
        for tile in row:
            print(str(tile).center(6), end = ' ')
        print('')

    print("\n  This is the end board after using a random strategy.")
    print("\n  The highest tile obtained is " + str(a.highestTile) + \
          ", after playing " + str(len(a.history)) + " moves.")

	# Consider better ways to report history
    # for e in a.history:
        # print(e)
