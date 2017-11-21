########################################################################
# Threes! is a game by by Asher Vollmer, Greg Wohlwend, Jimmy Hinson,  #
# and Hidden Variable. This is created so that AI/ML strategies for    #
# the game can be developed and tested easier, and is not intended as  #
# a replacement of the original game. Please support the developers by #
# purchasing their excellent game!                                     #
########################################################################


# I should make the note more detailed
"""This is the Threes Board class.
The board creation, game logic and record keeping are all in this file.
For testing AI strategy with Threes, you probably only need this."""


# Too elaborate comments
###########
# Imports #
###########


from __future__ import print_function
from random import random, randint
from math import ceil
from TileDeck import TileDeck
from copy import deepcopy


###########################################
# Helper functions for creating the board #
###########################################

# I should create a default size of 4.
# I should not create too much generality
def _create_board(size):
    """Generating the empty starting game board

    This board can be of any (nxn) size.
    0 = a space with no tile
    """

    board = []

# x and y are not used.
# I could compress this into an one-liner with list comprehension
    for x in range(size):
        row = []

        for y in range(size):
            row.append(0)
        board.append(row)

    return board

# Should add in the comments why the deck is returned as well.
def _populate_board(board, deck, nTiles):
    """Put the starting tiles on the board

    board should be list of list filled with 0's a la above function
    a deck, since Threes does not use a completely random tiles
    nTiles specify how many tiles you want
    """

# Move this below the test, so that in case test failure, I don't do any
# work.
    size = len(board)

# Need better English. It should have been:
# You can't plan to put more tiles on the board than there are spaces...
    # You can't have more tiles than spaces on the board
    if nTiles > size**2:
        # nTiles = size**2 #Silently resolve error
        raise TooManyTilesError

    for i in range(nTiles):
        tile = deck.get_next_tile()

# Need better comment?
        # Place tiles randomly on the board
        while True:
            pos = int(ceil(size**2 * random())) - 1
            x = pos // size
            y = pos % size

            if board[x][y] == 0:
                board[x][y] = tile
                break

    return board, deck


####################################
# Helper function for board swipes #
####################################


# I should move _reverse and _row2col below _swipe_left
def _reverse(board):
    """Reverse the board right and left"""

    for row in board:
        row.reverse()

    return board


# I should add comment that it's reflecting across x=y diagonal.
def _row2col(board):
    """Reflect across the diagonal"""

    new_board = board[:]  # make a new copy of the grid

    size = len(board)

    for x in range(size):
        for y in range(x):
            new_board[y][x], board[x][y] = board[x][y], new_board[y][x]

    return new_board


# I should put this first in this section, since this is the most
# important function here.
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


# I should specify that no tile means adding a tile = 0
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

# I should add the comment that the next tile is added on one of the
# rows that had tile movement in it.
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


########################
# Helper Function MISC #
########################


def _get_highest(board):
    """Return highest tile on the board, the board is a list of list

    Since the board unordered, you have to go through every element.
    """

    highest_tile = 3  # highest tile at the beginning of a game

    for row in board:
        for e in row:
            if e > highest_tile:
                highest_tile = e

    return highest_tile


# I should move expections up earlier, and explain what each is in a
# comment.
##############
# Exceptions #
##############


class NoMovementError:
    pass


class TooManyTilesError:
    pass


class InValidMoveError:
    pass


######################
# Threes Board Class #
######################


class ThreesBoard(object):
# Add 'contain' to the comments
    """The board, tiles and state of the game in Threes"""

    def __init__(
            self,
            size=4,  # standard Threes board size
            nTiles=9,  # standard Threes number of starting tiles
            board=[],  # empty or previous board
            deck=TileDeck(),  # new tile deck, or previous deck
            history=[],  # empty, or previous history
            nextTile=0):  # no tile, or previous tile

        """Creating the Threes board

        If passing in an old board position, that game will be recreated
        The tile deck will can also be recreated
        """

# Flipped logic. It would be better to use if board, and else.
        if not board:
            # Starting a new game; ignore previous history ... etc
            self.board = _create_board(size)
            self.deck = TileDeck([], 3)

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

        else:
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
            self.deck = TileDeck(deck.deck)
            self.history = history
            self.highestTile = _get_highest(self.board)

            # If old game information was incomplete
            if nextTile == 0:
                self.nextTile = self.deck.get_next_tile(0)

            else:
                self.nextTile = nextTile

    def swipe(self, move):
        """Same function for different swipes

        This will make recording keeping easier
        """

        direction = {'left': _swipe_left,
                     'right': _swipe_right,
                     'up': _swipe_up,
                     'down': _swipe_down}

        copy_board = deepcopy(self.board)

        try:
            copy_board = direction[move](copy_board, self.nextTile)

        except KeyError:
            raise InValidMoveError

# Too many checks to see if a move was made.
# I should just make the check here, and simply the _swipe_left function
        if self.board == copy_board:
            # raise NoMovementError
            pass

        else:
            self.board = copy_board
            self.highestTile = _get_highest(self.board)
            self.nextTile = self.deck.get_next_tile(self.highestTile)

# Typo
# I should have created a better archival system
            # Histoyr formate is: move, resulting board, next tile
            self.history.append((move, self.board, self.nextTile))

    def gameOver(self):
        new_board = deepcopy(self.board)

# The default is already 0, I should not have to add 0 again.
        if (_swipe_left(new_board, 0) == self.board and
                _swipe_right(new_board, 0) == self.board and
                _swipe_up(new_board, 0) == self.board and
                _swipe_down(new_board, 0) == self.board):
            return True

        return False

# I should also add a history check, this only check current and future
# conditions.
    def __eq__(self, other):
        return (self.board == other.board and
                self.deck == other.deck and
                self.nextTile == other.nextTile)

#I should use standard testing library
if __name__ == "__main__":

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
    import string

    a = ThreesBoard()

    while not a.gameOver():

        # print "The next tile is :", a.nextTile
        # for row in a.board:
            # print row

        nextMove = 'blank'
        moves = {'w': 'up',
                 'a': 'left',
                 's': 'down',
                 'd': 'right'}

        # while nextMove not in moves.keys():
        #   nextMove = raw_input()

        # try: a.swipe(moves[nextMove])

        try:
            move = choice(list(moves.keys()))
            a.swipe(moves[move])

        except NoMovementError:
            pass

    print("\n  The next tile is :", a.nextTile, '\n')
    for row in a.board:
        for tile in row:
# I believe string.center is no longer valid in python3
# I should change it so that it works well in both python2 and 3
            print(string.center(str(tile), 6, ' '), end=' ')
        print('')

    print("\n  This is the end board after using a random strategy.")
    print("\n  The highest tile obtained is " + str(a.highestTile) + \
          ", after playing " + str(len(a.history)) + " moves.")

# I should create a better way to tell the history of the game
    for e in a.history:
        print(e)
