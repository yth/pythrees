########################################################################
# Threes! is a game by by Asher Vollmer, Greg Wohlwend, Jimmy Hinson,  #
# and Hidden Variable. This is created so that AI/ML strategies for    #
# the game can be developed and tested easier, and is not intended as  #
# a replacement of the original game. Please support the developers by #
# purchasing their excellent game!                                     #
########################################################################


'''This is the Threes Board class.
The board creation, game logic and record keeping are all in this file.
For testing AI strategy with Threes, you probably only need this.'''


###########
# Imports #
###########


from random import random, randint
from math import ceil
from TileDeck import TileDeck
from copy import deepcopy

###########################################
# Helper functions for creating the board #
###########################################


def _createBoard(size):
    '''Generating the empty starting game board

    This board can be of any (nxn) size.
    0 = a space with no tile
    '''

    board = []

    for x in range(size):
        row = []

        for y in range(size):
            row.append(0)
        board.append(row)
    return board


def _populateBoard(board, deck, nTiles):
    '''Put the starting tiles on the board

    board should be list of list filled with 0's a la above function
    a deck, since Threes does not use a completely random tiles
    nTiles specify how many tiles you want
    '''

    size = len(board)

    # You can't have more tiles than spaces on the board
    if nTiles > size**2:
        # nTiles = size**2 #Silently resolve error
        raise TooManyTilesError

    for i in range(nTiles):
        tile = deck.getNextTile()

        # Place tiles randomly on the board
        while True:
            pos = int(ceil(size**2 * random())) - 1
            x = pos / size
            y = pos % size

            if board[x][y] == 0:
                board[x][y] = tile
                break

    return board, deck

####################################
# Helper function for board swipes #
####################################


def _reverse(board):
    '''Reverse the board right and left'''

    for row in board:
        row.reverse()

    return board


def _row2col(board):
    '''Reflect across the diagonal'''

    new_board = board[:]  # make a new copy of the grid

    size = len(board)

    for x in range(size):
        for y in range(x):
            new_board[y][x], board[x][y] = board[x][y], new_board[y][x]

    return new_board


def _shiftLeft(row):
    '''Performs what happen at row level when you swipe left in Threes

    Adding next tile does not happen at this level.
    '''

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


def _swipeLeft(board, tile=0):
    '''Perform what happens at board level when you swipe left

    Adds the next tile
    Add no tile by default
    '''

    copy_board = deepcopy(board)

    for row in copy_board:
        row = _shiftLeft(row)

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


def _swipeRight(board, tile):
    '''Perform what happens at board level when you swipe right

    Based on _swipeLeft
    '''

    new_board = _reverse(_swipeLeft(_reverse(board), tile))

    return new_board


def _swipeUp(board, tile):
    '''Perform what happens at board level when you swipe up

    Based on _swipeLeft
    '''

    new_board = _row2col(_swipeLeft(_row2col(board), tile))

    return new_board


def _swipeDown(board, tile):
    '''Perform what happens at board level when you swipe down

    Based on _swipeLeft
    '''

    new_board = _row2col(_swipeRight(_row2col(board), tile))

    return new_board


########################
# Helper Function MISC #
########################


def _getHighest(board):
    '''Return highest tile on the board, the board is a list of list

    Since the board unordered, you have to go through every element.
    '''

    highest_tile = 3  # highest tile at the beginning of a game

    for row in board:
        for e in row:
            if e > highest_tile:
                highest_tile = e

    return highest_tile


##############
# Exceptions #
##############


class NoMovementError:
    pass


class TooManyTilesError:
    pass


######################
# Threes Board Class #
######################


class ThreesBoard(object):
    '''The board, tiles and state of the game in Threes'''

    def __init__(self,
                 size=4,  # standard Threes board size
                 nTiles=9,  # standard Threes number of starting tiles
                 board=[],  # empty or previous board
                 deck=TileDeck(),  # new tile deck, or previous deck
                 history=[],  # empty, or previous history
                 nextTile=0):  # no tile, or previous tile
        '''Creating the Threes board

        If passing in an old board position, that game will be recreated
        The tile deck will can also be recreated
        '''

        if not board:
            # Starting a new game; ignore previous history ... etc
            self.board = _createBoard(size)
            self.deck = TileDeck([], 3)

            # Populating a new board with start up tiles
            self.board, self.deck = _populateBoard(self.board,
                                                   self.deck,
                                                   nTiles)

            self.nextTile = self.deck.getNextTile()

            # Set up empty history, then set initial condition
            self.history = []

            # history formate is: move, resulting board, next tile)
            self.history.append(('start', self.board, self.nextTile))
            self.highestTile = 3

        else:
            '''To consider: store all information in history
                            eliminate the need for old boards, decks ...
                            initialize a previous game in form of
                            board = history[1]
                            nextTile = history[2]
                            ... etc
                            For next major version?
            '''

            # Passing in the old game; size, ntiles are all ignored
            self.board = board
            self.deck = TileDeck(deck.deck)
            self.history = history
            self.highestTile = _getHighest(self.board)

            # If old game information was incomplete
            if nextTile == 0:
                self.nextTile = self.deck.getNextTile(0)

            else:
                self.nextTile = nextTile

    def swipe(self, move):
        '''Same function for different swipes

        This will make recording keeping easier
        '''

        direction = {'left' : _swipeLeft,
                     'right': _swipeRight,
                     'up'   : _swipeUp,
                     'down' : _swipeDown}

        copy_board = deepcopy(self.board)

        try:
            copy_board = direction[move](copy_board, self.nextTile)

        except KeyError:
            return "Not a valid move."

        if self.board == copy_board:
            # raise NoMovementError
            pass

        else:
            self.board = copy_board
            self.highestTile = _getHighest(self.board)
            self.nextTile = self.deck.getNextTile(self.highestTile / 8)

            # Histoyr formate is: move, resulting board, next tile
            self.history.append((move, self.board, self.nextTile))

    def gameOver(self):
        new_board = deepcopy(self.board)

        if _swipeLeft (new_board, 0) == self.board and \
           _swipeRight(new_board, 0) == self.board and \
           _swipeUp   (new_board, 0) == self.board and \
           _swipeDown (new_board, 0) == self.board:

            return True

        return False

    def __eq__(self, other):
        return self.board == other.board and \
               self.deck == other.deck and \
               self.nextTile == other.nextTile

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
            move = choice(moves.keys())
            a.swipe(moves[move])

        except NoMovementError:
            pass

    print "\n  The next tile is :", a.nextTile, '\n'
    for row in a.board:
        for tile in row:
            print string.center(str(tile), 6, ' '),
        print ''

    print "\n  This is the end board after using a random strategy."
    print "\n  The highest tile obtained is " + str(a.highestTile) + \
          ", after playing " + str(len(a.history)) + " moves."

    # print a.history
