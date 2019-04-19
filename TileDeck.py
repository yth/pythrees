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

from random import shuffle
from copy import copy


######################
# Important Constant #
######################


_BASE = [
    1, 1, 1, 1,
    2, 2, 2, 2,
    3, 3, 3, 3
]

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


def _create_deck(highest_tile=3):
    """Tiles to come in a game of Threes.

    After a certain tile value is achieved on the board, bonus tiles
    start to be added after every 2 stacks. In this version, this
    behavior will be hard coded in. I wonder if the actual game flips a
    coin after every tile deck is used up.

    The highest bonus tile is 1/8 of the current highest tile on the
    board. The smallest bonus tile is 6. When the smallest bonus tile is
    allowed to be created, bonus tiles comes into effect.

    There are a maximum of possible bonus tiles. Their values are 1/8,
    1/16, and 1/32 of the highest tile on the board. Only bonus tile
    value greater than 6 shows up as a possible choice. One of these
    tiles is added to the board like a regular tile after a swipe. It's
    random which one is added.

    We just add the tile to the head of our standard deck. The display
    will handle showing all possible bonus tiles.

    The standard deck are two base decks that are shuffled and then
    combined
    """

    deck = []

    # Create bonus title
    bonus_deck = []

    while highest_tile >= 48 and len(bonus_deck) < 4:
        bonus_deck.append(highest_tile/8)
        highest_tile /= 2

    if bonus_deck:
        shuffle(bonus_deck)
        deck.append(bonus_deck.pop())

    # Prevent too many of the same tile in a row too often
    sequence1 = copy(_BASE)
    sequence2 = copy(_BASE)

    shuffle(sequence1)
    shuffle(sequence2)

    # original deck can be [] or contain a bonus tile
    deck += sequence1 + sequence2

    return copy(deck)

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
