########################################################################
# Threes! is a game by by Asher Vollmer, Greg Wohlwend, Jimmy Hinson,  #
# and Hidden Variable. This is created so that AI/ML strategies for    #
# the game can be developed and tested easier, and is not intended as  #
# a replacement of the original game. Please support the developers by #
# purchasing their excellent game!                                     #
########################################################################


"""
This is the tile deck used by Threes to the best of my knowledge.
"""


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
another is created.
"""

####################
# Helper Functions #
####################


def _create_deck(highest_tile=3):
    """Tiles to come in a game of Threes.

    Bonus tiles gets added every 2 stacks. Highest bonus tile is 1/8 of
    the current highest tile on the board. You have equal chance of
    getting 1 of 3 tiles. The 2 tiles besides the highest are 1/16 and
    1/32 of the highest tile on the board. The smallest possible bonus
    tile is 6. If a bonus tile value is less than 6, none is created for
    that slot.

    This create a deck of 2 stacks, with the bonus tile if appropriate.
    Bonus tile is the first tile, if there is a bonus tile.
    First deck of a game never have a bonus tile.
    """

    from random import shuffle
    from random import randint

    deck = []
    max_bonus = highest_tile / 8

    # Check if a bonus tile needs to be created
    if max_bonus % 6 == 0 and max_bonus > 3:

        # Create up to 3 bonus tiles, if the max_bonus is highest enough
        bonus = [max_bonus]

        if max_bonus / 2 > 3:
            bonus.append(max_bonus / 2)

            if max_bonus / 4 > 3:
                bonus.append(max_bonus / 4)

        deck = [bonus[randint(0, len(bonus) - 1)]]  # Bonus tile

    sequence1 = _BASE[:]
    sequence2 = _BASE[:]

    shuffle(sequence1)
    shuffle(sequence2)

    # original deck can be [] or contain a bonus tile
    deck += sequence1 + sequence2

    return deck

##################
# TileDeck Class #
##################


class TileDeck(object):
    """Tile deck used in a game of Threes"""

    def __init__(self, existing_deck=[], max_bonus=3):
        """Generating a tile deck to be used in a game of threes

        max_bonus: depending on the highest score in game
        existing_deck: normally empty - starting a new game
                       if not empty - it means it's starting an previous
                                      game, and need the old deck again
        """

        if not existing_deck:
            # Create a new deck, if not using an existing one
            self.deck = _create_deck(max_bonus)

        else:
            # Use an existing deck
            self.deck = existing_deck

    def get_next_tile(self, highest_tile=3):
        """Get the next tile in FIFO order due to bonus tile placement

        highest_tile: on the game board, the max bonus is 1/8 of it
        """

        try:
            return self.deck.pop(0)

        except IndexError:
            # Make a draw a new deck if the old one runs out
            self.deck = _create_deck(highest_tile / 8)
            return self.deck.pop(0)

    def __str__(self):
        """A peek at the deck"""

        return '<Current Deck: ' + str(self.deck) + '>'

    def __repr__(self):
        """Tile Deck as a string"""

        return 'TileDeck(' + str(self.deck) + ', 0)'

    def __eq__(self, other):
        """Check equality"""

        return self.deck == other.deck

# Basic Testing
if __name__ == '__main__':

    # deck = TileDeck()
    # print len(deck.deck)
    # print deck.deck

    def simpleTest():
        deck0 = TileDeck()
        deck1 = TileDeck([], 3)  # new deck
        deck2 = TileDeck([], 3)  # wrong bonus
        deck3 = TileDeck([1, 2, 3], 12)  # right bonus, existing deck
        deck4 = TileDeck([], 3)
        deck5 = TileDeck([], 192)  # right bonus

        print deck0
        print deck1
        print deck2
        print deck3
        print deck4
        print deck5

        print repr(deck1)
        print str(deck1)

        deck5 = eval(repr(deck2))
        assert deck5 == deck2

        for i in range(len(deck2.deck)):
            print deck2.get_next_tile(),

        print deck2.get_next_tile()

    # simpleTest()
