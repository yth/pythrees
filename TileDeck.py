########################################################################
# Threes! is a game by by Asher Vollmer, Greg Wohlwend, Jimmy Hinson,  #
# and Hidden Variable. This is created so that AI/ML strategies for    #
# the game can be developed and tested easier, and is not intended as  #
# a replacement of the original game. Please support the developers by #
# purchasing their excellent game!                                     #
########################################################################


""" Tile Deck

This is the tile deck used by Threes to the best of my knowledge.
"""


###########
# Imports #
###########

# Future imports must occur at the beginning of a file
from __future__ import print_function


import random
import copy


######################
# Important Constant #
######################


_BASE = (
    1, 1, 1, 1,
    2, 2, 2, 2,
    3, 3, 3, 3
)

"""
The next tile given to you is not completely random. It's drawn without
replacement from a shuffled deck with above tiles. When you run out,
another is created. I think this can be implemented in two different
ways without affect the how the game is emulated. One way is to shuffle
a copy of the list and then draw in order. Another is to pop off a
random tile.
"""

####################
# Helper Functions #
####################

def _create_bonus_deck(highest_tile=3):
    """Bonus Deck for game of Threes!

    The smallest bonus tile is 6. The maximum number of tiles in a bonus
    deck is 3. The values of the bonus deck tiles are 1/8, 1/16 and 1/32
	of the highest tile value on the board. If any of the bonus deck
    tile values would be smaller than 6, no bonus tile is created for
    that tile slot in the bonus deck.

    e.g. highest_tile=3 => bonus_deck = []
    e.g. highest_tile=12 => bonus_deck = []
    e.g. highest_tile=48 => bonus_deck = [6]
    e.g. highest_tile=96 => bonus_deck = [12, 6]
    e.g. highest_tile=192 => bonus_deck = [24, 12, 6]
    e.g. highest_tile=384 => bonus_deck = [48, 24, 12]
    """

    bonus_deck = []
    while highest_tile >= 48 and len(bonus_deck) < 3:
        bonus_deck.append(highest_tile//8)
        highest_tile //= 2

    return bonus_deck

def _create_deck(highest_tile=3):
    """Tiles to come in a game of Threes.

    The standard deck are two base decks that are shuffled and then
    combined
    """
    deck = []
    bonus_deck = _create_bonus_deck(highest_tile)

    if bonus_deck:
        deck.append(bonus_deck)

    # Prevent too many of the same tile in a row too often
    sequence1 = copy.copy(list(_BASE))
    sequence2 = copy.copy(list(_BASE))

    random.shuffle(sequence1)
    random.shuffle(sequence2)

    # original deck can be [] or contain a bonus tile
    deck += sequence1 + sequence2

    return deck

def _create_deck_2():
    """Tiles in a Threes! tile deck

    It represent all the tiles that can be drawn from a fresh deck.
    """

    return copy.copy(list(_BASE))

##################
# TileDeck Class #
##################


class TileDeck(object):
    """Tile deck used in a game of Threes"""

    def __init__(self, existing_deck=None, highest_tile=3):
        """Generating a tile deck to be used in a game of threes

        highest_tile: depending on the highest score in game
        existing_deck: normally empty - starting a new game
                       if not empty - it means it's starting an previous
                                      game, and need the old deck again
        """

        if existing_deck:
            self.deck = existing_deck
        else:
            self.deck = _create_deck(highest_tile)

    def get_next_tile(self, highest_tile=3):
        """Get the next tile in FIFO order due to bonus tile placement

        highest_tile: on the game board, the max bonus is 1/8 of it
        """

        try:
            return self.deck.pop(0)

        except IndexError:
            # Make a draw a new deck if the old one runs out
            self.deck = _create_deck(highest_tile)
            return self.deck.pop(0)

    def __str__(self):
        """A peek at the deck"""

        return '<Current Deck: ' + str(self.deck) + '>'

    def __repr__(self):
        """Tile Deck as a string"""

        return 'TileDeck(' + str(self.deck) + ')'

    def __eq__(self, other):
        """Check equality"""

        return self.deck == other.deck

# Basic Testing
if __name__ == '__main__':

    # Imports

    # TODO: Create basic testing facility using one of Python's builtin
    # test framework

    # Simplest test
    deck = TileDeck()
    print(len(deck.deck))
    print(deck.deck)

    def simpleTest():
        deck0 = TileDeck()
        deck1 = TileDeck([], 3)  # new deck
        deck2 = TileDeck([], 3)  # wrong bonus
        deck3 = TileDeck([1, 2, 3], 12)  # right bonus, existing deck
        deck4 = TileDeck([], 3)
        deck5 = TileDeck([], 192)  # right bonus

        print(deck0)
        print(deck1)
        print(deck2)
        print(deck3)
        print(deck4)
        print(deck5)

        print(repr(deck1))
        print(str(deck1))

        deck5 = eval(repr(deck2))
        assert deck5 == deck2

        for i in range(len(deck2.deck)):
            print(deck2.get_next_tile(), end=' ')

        print(deck2.get_next_tile())

    simpleTest()
